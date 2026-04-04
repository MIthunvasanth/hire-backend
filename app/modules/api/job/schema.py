from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str
    skills: list[str]


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    skills: list[str] | None = None


class JobResponse(BaseModel):
    id: str
    title: str
    description: str
    skills: list[str]
