from pydantic import BaseModel, EmailStr, Field


class AuthRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str


class AuthTokenResponse(BaseModel):
    access_token: str
    user: AuthUserResponse
