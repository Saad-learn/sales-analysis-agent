from app.workers.celery_app import celery_app
from app.services.ai_service import AIService

ai_service = AIService()

@celery_app.task(name="analyze_email_task")
def analyze_email_task(email_text: str):
    import asyncio
    return asyncio.run(ai_service.analyze_email(email_text))