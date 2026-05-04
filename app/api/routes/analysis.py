from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.analysis import EmailAnalysis

router = APIRouter()

@router.get("/{email_id}")
def get_analysis(email_id: int, db: Session = Depends(get_db)):
    total = db.query(EmailAnalysis).count()
    print("TOTAL ANALYSIS ROWS:", total)

    result = (
        db.query(EmailAnalysis)
        .filter(EmailAnalysis.email_id == email_id)
        .order_by(EmailAnalysis.id.desc())
        .first()
    )

    if not result:
        return {
            "message": "not found",
            "total": total,
            "email_id": email_id
        }

    return {
        "id": result.id,
        "email_id": result.email_id,
        "sentiment": result.sentiment,
        "budget": result.budget,
        "authority": result.authority,
        "need": result.need,
        "timeline": result.timeline,
        "score": result.score,
        "summary": result.summary,
    }
