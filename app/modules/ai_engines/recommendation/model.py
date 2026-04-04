from datetime import datetime

from pydantic import BaseModel


class RecommendationModel(BaseModel):
    candidate_id: str
    job_id: str | None = None
    items: list[str] = []
    created_at: datetime = datetime.utcnow()
