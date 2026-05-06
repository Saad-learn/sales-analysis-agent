from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base

class EmailAnalysis(Base):
    __tablename__ = "email_analysis"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), index=True)
    sentiment = Column(String)
    budget = Column(String)
    authority = Column(String)
    need = Column(String)
    timeline = Column(String)
    score = Column(Float)
    summary = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)