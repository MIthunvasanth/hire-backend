from fastapi import APIRouter

from . import service
from .schema import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/")
async def create_user(payload: UserCreate):
    user_id = await service.create_user_service(payload.model_dump())
    return {"id": user_id}


@router.get("/")
async def list_users():
    return await service.list_users_service()


@router.get("/{user_id}")
async def get_user(user_id: str):
    return await service.get_user_service(user_id)


@router.put("/{user_id}")
async def update_user(user_id: str, payload: UserUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_user_service(user_id, update_data)
    return {"message": "updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    await service.delete_user_service(user_id)
    return {"message": "deleted"}
