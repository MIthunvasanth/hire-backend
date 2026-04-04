from datetime import datetime

from pydantic import BaseModel


class RecruiterModel(BaseModel):
    user_id: str
    company: str | None = None
    created_at: datetime = datetime.utcnow()
