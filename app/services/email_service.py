from sqlalchemy.exc import IntegrityError
from app.models.email import Email


class EmailService:
    @staticmethod
    def create_email(db, **kwargs):
        gmail_id = kwargs.get("gmail_message_id")

        if not gmail_id:
            return None

        existing = db.query(Email).filter(
            Email.gmail_message_id == gmail_id
        ).first()

        if existing:
            return existing

        email = Email(**kwargs)
        db.add(email)

        try:
            db.commit()
            db.refresh(email)
            return email
        except IntegrityError:
            db.rollback()
            return db.query(Email).filter(
                Email.gmail_message_id == gmail_id
            ).first()
        except Exception:
            db.rollback()
            return None