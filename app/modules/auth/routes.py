from fastapi import APIRouter, HTTPException

from .schema import AuthLogin, AuthRegister, AuthTokenResponse
from . import service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthTokenResponse, status_code=201)
async def register(payload: AuthRegister):
    try:
        return await service.register_service(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=AuthTokenResponse)
async def login(payload: AuthLogin):
    try:
        return await service.login_service(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
