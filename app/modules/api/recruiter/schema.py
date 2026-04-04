from pydantic import BaseModel


class RecruiterCreate(BaseModel):
    user_id: str
    company: str | None = None


class RecruiterUpdate(BaseModel):
    company: str | None = None


class RecruiterResponse(BaseModel):
    id: str
    user_id: str
    company: str | None = None
