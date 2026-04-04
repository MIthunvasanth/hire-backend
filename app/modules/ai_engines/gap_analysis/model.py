from datetime import datetime

from pydantic import BaseModel


class GapAnalysisModel(BaseModel):
    candidate_id: str
    job_id: str
    missing_skills: list[str] = []
    created_at: datetime = datetime.utcnow()
