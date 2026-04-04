from datetime import datetime

from pydantic import BaseModel


class InterviewModel(BaseModel):
    application_id: str
    scheduled_at: datetime | None = None
    status: str = "scheduled"
    created_at: datetime = datetime.utcnow()
