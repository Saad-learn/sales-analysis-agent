from app.workers.celery_app import celery_app

@celery_app.task(name="fetch_user_emails_task")
def fetch_user_emails_task(user_id: int):
    return {
        "user_id": user_id,
        "emails": []
    }