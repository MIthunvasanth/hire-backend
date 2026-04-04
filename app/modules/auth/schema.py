from pydantic import BaseModel


class AuthRegister(BaseModel):
    email: str
    password: str


class AuthLogin(BaseModel):
    email: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
