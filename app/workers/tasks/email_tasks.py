import os
import logging
from app.workers.celery_app import celery_app
from app.workers.tasks.analysis_tasks import analyze_email_task
from app.db.database import SessionLocal
from app.models.user import User
from app.services.gmail_service import GmailService
from app.services.email_service import EmailService
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)

def _get_valid_credentials(user: User, db) -> Credentials:
    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        user.access_token = credentials.token
        user.token_expiry = credentials.expiry
        db.commit()

    return credentials


@celery_app.task(name="fetch_user_emails_task")
def fetch_user_emails_task(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"status": "error", "message": f"User {user_id} not found"}

        if not user.access_token:
            return {"status": "error", "message": "No access token for user"}

        credentials = _get_valid_credentials(user, db)
        gmail = GmailService(credentials=credentials)
        messages = gmail.list_messages(max_results=10)

        processed = 0
        for msg_ref in messages:
            raw_message = gmail.get_message(msg_ref["id"])
            email_data = gmail.extract_email_data(raw_message)

            saved_email = EmailService.create_email(
                db,
                user_id=user_id,
                gmail_message_id=msg_ref["id"],
                subject=email_data.get("subject", ""),
                sender=email_data.get("sender", ""),
                body=email_data.get("body", ""),
            )

            if saved_email:
                analyze_email_task.delay(saved_email.id, email_data.get("body", ""))
                processed += 1

        return {"status": "success", "user_id": user_id, "emails_processed": processed}
    except Exception as e:
        db.rollback()
        logger.error(f"Error in fetch_user_emails_task: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()