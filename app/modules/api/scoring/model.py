from datetime import datetime

from pydantic import BaseModel


class ScoringModel(BaseModel):
    application_id: str
    score: float
    created_at: datetime = datetime.utcnow()
