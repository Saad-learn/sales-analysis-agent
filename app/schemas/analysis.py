from typing import Optional
from pydantic import BaseModel, field_validator

class BantSchema(BaseModel):
    budget: Optional[str] = None
    authority: Optional[str] = None
    need: Optional[str] = None
    timeline: Optional[str] = None
    @field_validator(
        "budget",
        "authority",
        "need",
        "timeline",
        mode="before"
    )
    def clean_values(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            if value.lower() in {
                "",
                "null",
                "none",
                "n/a",
                "not mentioned",
                "unknown"
            }:
                return None
            return value
        return str(value)

class EmailAnalysis(BaseModel):
    sentiment: str = "neutral"
    bant: BantSchema = BantSchema()
    score: float = 0.0
    summary: str = "No summary generated"
    @field_validator("sentiment", mode="before")
    def validate_sentiment(cls, value):
        allowed = {"positive", "negative", "neutral"}
        if not value:
            return "neutral"
        value = str(value).strip().lower()
        return value if value in allowed else "neutral"
    @field_validator("score", mode="before")
    def validate_score(cls, value):
        try:
            value = float(value)
        except Exception:
            return 0.0
        if value < 0:
            return 0.0
        if value > 100:
            return 100.0
        return value
    @field_validator("summary", mode="before")
    def validate_summary(cls, value):
        if not value:
            return "No summary generated"
        if not isinstance(value, str):
            return str(value)
        return value.strip()