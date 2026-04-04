from datetime import datetime

from pydantic import BaseModel


class ApplicationModel(BaseModel):
    candidate_id: str
    job_id: str
    status: str = "applied"
    created_at: datetime = datetime.utcnow()
