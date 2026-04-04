from pydantic import BaseModel


class GapAnalysisCreate(BaseModel):
    candidate_id: str
    job_id: str
    missing_skills: list[str] = []


class GapAnalysisUpdate(BaseModel):
    missing_skills: list[str] | None = None


class GapAnalysisResponse(BaseModel):
    id: str
    candidate_id: str
    job_id: str
    missing_skills: list[str]
