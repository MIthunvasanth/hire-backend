from datetime import datetime

from pydantic import BaseModel


class CandidateModel(BaseModel):
    user_id: str
    headline: str | None = None
    skills: list[str] = []
    created_at: datetime = datetime.utcnow()
