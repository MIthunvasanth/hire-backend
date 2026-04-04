from datetime import datetime

from pydantic import BaseModel


class JobModel(BaseModel):
    title: str
    description: str
    skills: list[str]
    created_at: datetime = datetime.utcnow()
