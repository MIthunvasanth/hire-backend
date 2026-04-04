from datetime import datetime

from pydantic import BaseModel


class ResumeModel(BaseModel):
    candidate_id: str
    content: str
    created_at: datetime = datetime.utcnow()
