from pydantic import BaseModel, Field


class StudySubModule(BaseModel):
    id: str
    title: str
    description: str | None = None
    completed: bool = False


class StudyModuleTest(BaseModel):
    id: str
    title: str
    type: str = "interview"  # "interview" | "coding"
    questions: list[str] = []
    description: str | None = None
    completed: bool = False


class StudyTask(BaseModel):
    id: str
    title: str
    resource: str | None = None
    completed: bool = False
    submodules: list[StudySubModule] = []


class StudyDayPlan(BaseModel):
    day: int
    topic: str
    tasks: list[StudyTask] = []
    module_test: StudyModuleTest | None = None
    overall_test: StudyModuleTest | None = None


class StudyPlanGenerateRequest(BaseModel):
    gap_analysis_id: str
    user_id: str | None = None
    user_email: str | None = None


class StudyPlanResponse(BaseModel):
    id: str
    gap_analysis_id: str
    user_id: str | None = None
    user_email: str | None = None
    title: str
    summary: str
    plan: list[StudyDayPlan] = []
    created_at: str


class StudyPlanTaskUpdateRequest(BaseModel):
    completed: bool


class StudyPlanHistoryResponse(BaseModel):
    plans: list[StudyPlanResponse] = Field(default_factory=list)
