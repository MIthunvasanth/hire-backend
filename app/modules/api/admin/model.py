from datetime import datetime

from pydantic import BaseModel


class AdminModel(BaseModel):
    user_id: str
    created_at: datetime = datetime.utcnow()
