from datetime import datetime

from pydantic import BaseModel


class InterviewCreate(BaseModel):
    application_id: str
    scheduled_at: datetime | None = None
    status: str = "scheduled"


class InterviewUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: str | None = None


class InterviewResponse(BaseModel):
    id: str
    application_id: str
    scheduled_at: datetime | None = None
    status: str


class InterviewAgentNextRequest(BaseModel):
    role: str
    level: str | None = None
    skills: list[str] = []
    last_answer: str | None = None


class InterviewAgentNextResponse(BaseModel):
    interview_id: str
    question: str
    turn: int
