from pydantic import BaseModel


class ResumeCreate(BaseModel):
    candidate_id: str
    content: str


class ResumeUpdate(BaseModel):
    content: str | None = None


class ResumeResponse(BaseModel):
    id: str
    candidate_id: str
    content: str
