from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.workers.tasks.email_tasks import fetch_user_emails_task

router = APIRouter()

@router.post("/fetch/{user_id}")
def fetch_gmail_emails(user_id: int, db: Session = Depends(get_db)):
    """Trigger background Gmail fetch task"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Google OAuth login required first",
        )
    task = fetch_user_emails_task.delay(user_id)
    return {
        "message": "Email fetching started",
        "task_id": task.id,
    }