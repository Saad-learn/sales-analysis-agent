import asyncio
import logging
from app.workers.celery_app import celery_app
from app.services.ai_service import AIService
from app.db.database import SessionLocal
from app.models.analysis import EmailAnalysis
from app.services.extractors.budget import extract_budget
from app.services.extractors.authority import extract_authority
from app.services.extractors.need import extract_need
from app.services.extractors.timeline import extract_timeline

logger = logging.getLogger(__name__)
ai_service = AIService()


@celery_app.task(name="analyze_email_task")
def analyze_email_task(email_id: int, email_text: str):
    
    if not email_text:
        return {"status": "error", "message": "No text provided"}

    try:
        ai_result = asyncio.run(ai_service.analyze_email(email_text))
    except Exception as e:
        logger.error(f"AI Service Failure: {e}")
        ai_result = {}

    regex_results = {
        "budget": extract_budget(email_text),
        "authority": extract_authority(email_text),
        "need": extract_need(email_text),
        "timeline": extract_timeline(email_text),
    }

    def get_best_value(key):
        ai_val = ai_result.get(key)
        if ai_val and ai_val not in ("unknown", "Not mentioned"):
            return str(ai_val)
        reg_val = regex_results[key].get("value")
        return str(reg_val) if reg_val else "unknown"

    db = SessionLocal()
    try:
        existing = db.query(EmailAnalysis).filter(EmailAnalysis.email_id == email_id).first()
        if existing:
            return {"status": "skipped", "email_id": email_id, "message": "Already analyzed"}

        analysis = EmailAnalysis(
            email_id=email_id,
            sentiment=ai_result.get("sentiment", "neutral"),
            budget=get_best_value("budget"),
            authority=get_best_value("authority"),
            need=get_best_value("need"),
            timeline=get_best_value("timeline"),
            score=float(ai_result.get("score", 0.0)),
            summary=ai_result.get("summary", "Analysis completed"),
        )
        db.add(analysis)
        db.commit()
        return {"status": "success", "email_id": email_id}
    except Exception as e:
        db.rollback()
        logger.error(f"Database Error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()