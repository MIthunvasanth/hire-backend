from pydantic import BaseModel


class TeacherSessionCreate(BaseModel):
    user_id: str
    topic: str


class TeacherSessionResponse(BaseModel):
    id: str
    user_id: str
    topic: str
    status: str
