from pydantic import BaseModel


class ScoringCreate(BaseModel):
    application_id: str
    score: float


class ScoringUpdate(BaseModel):
    score: float | None = None


class ScoringResponse(BaseModel):
    id: str
    application_id: str
    score: float
