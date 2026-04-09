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


class GapJobPayload(BaseModel):
    id: str
    title: str
    company: str
    location: str | None = None
    type: str | None = None
    description: str | None = None
    skills: list[str] = []
    salary: str | None = None


class GapAnalyzeRequest(BaseModel):
    user_id: str | None = None
    user_email: str | None = None
    job: GapJobPayload


class GapSkillBar(BaseModel):
    name: str
    value: int


class GapActionPlanItem(BaseModel):
    title: str
    reason: str
    next_steps: list[str] = []
    priority: str | None = None


class GapAnalyzeResponse(BaseModel):
    id: str
    match_score: int = 0
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    weak_skills: list[str] = []
    skill_bars: list[GapSkillBar] = []
    insights: str = ""
    role_fit_summary: str = ""
    missing_explanations: list[str] = []
    strengths: list[str] = []
    interview_risks: list[str] = []
    action_plan: list[GapActionPlanItem] = []
    job: GapJobPayload


class GapAnalysisHistoryItem(GapAnalyzeResponse):
    created_at: str
    user_id: str | None = None
    user_email: str | None = None
