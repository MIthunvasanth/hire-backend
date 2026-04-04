from fastapi import APIRouter, HTTPException

from .schema import AuthLogin, AuthRegister
from . import service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(payload: AuthRegister):
    try:
        token = await service.register_service(payload.model_dump())
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(payload: AuthLogin):
    try:
        token = await service.login_service(payload.model_dump())
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
