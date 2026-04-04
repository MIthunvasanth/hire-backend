from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    candidate_id: str
    job_id: str


class ApplicationUpdate(BaseModel):
    status: str | None = None


class ApplicationResponse(BaseModel):
    id: str
    candidate_id: str
    job_id: str
    status: str
