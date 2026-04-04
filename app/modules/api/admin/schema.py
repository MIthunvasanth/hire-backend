from pydantic import BaseModel


class AdminCreate(BaseModel):
    user_id: str


class AdminUpdate(BaseModel):
    user_id: str | None = None


class AdminResponse(BaseModel):
    id: str
    user_id: str
