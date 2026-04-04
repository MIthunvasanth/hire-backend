from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    role: str = "user"


class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None
    role: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
