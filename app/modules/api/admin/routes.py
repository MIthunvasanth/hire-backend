from fastapi import APIRouter

from . import service
from .schema import AdminCreate, AdminUpdate

router = APIRouter(prefix="/admins", tags=["Admin"])


@router.post("/")
async def create_admin(payload: AdminCreate):
    admin_id = await service.create_admin_service(payload.model_dump())
    return {"id": admin_id}


@router.get("/")
async def list_admins():
    return await service.list_admins_service()


@router.get("/{admin_id}")
async def get_admin(admin_id: str):
    return await service.get_admin_service(admin_id)


@router.put("/{admin_id}")
async def update_admin(admin_id: str, payload: AdminUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_admin_service(admin_id, update_data)
    return {"message": "updated"}


@router.delete("/{admin_id}")
async def delete_admin(admin_id: str):
    await service.delete_admin_service(admin_id)
    return {"message": "deleted"}
