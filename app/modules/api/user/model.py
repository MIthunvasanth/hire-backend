from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    email: str
    name: str
    role: str = "user"
    created_at: datetime = datetime.utcnow()
