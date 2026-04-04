from pydantic import BaseModel


class RecommendationCreate(BaseModel):
    candidate_id: str
    job_id: str | None = None
    items: list[str] = []


class RecommendationUpdate(BaseModel):
    items: list[str] | None = None


class RecommendationResponse(BaseModel):
    id: str
    candidate_id: str
    job_id: str | None = None
    items: list[str]
