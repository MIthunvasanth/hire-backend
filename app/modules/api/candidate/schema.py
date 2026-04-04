from pydantic import BaseModel


class CandidateCreate(BaseModel):
    user_id: str
    headline: str | None = None
    skills: list[str] = []


class CandidateUpdate(BaseModel):
    headline: str | None = None
    skills: list[str] | None = None


class CandidateResponse(BaseModel):
    id: str
    user_id: str
    headline: str | None = None
    skills: list[str]
