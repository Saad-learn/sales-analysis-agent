from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmailBase(BaseModel):
    subject: Optional[str]
    sender: Optional[str]
    snippet: Optional[str]
    body: Optional[str]

class EmailCreate(EmailBase):
    user_id: int
    gmail_message_id: str

class EmailResponse(EmailBase):
    id: int
    user_id: int
    gmail_message_id: str
    received_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True