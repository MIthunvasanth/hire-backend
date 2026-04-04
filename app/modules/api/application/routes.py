from fastapi import APIRouter

from . import service
from .schema import ApplicationCreate, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["Application"])


@router.post("/")
async def create_application(payload: ApplicationCreate):
    application_id = await service.create_application_service(payload.model_dump())
    return {"id": application_id}


@router.get("/")
async def list_applications():
    return await service.list_applications_service()


@router.get("/{application_id}")
async def get_application(application_id: str):
    return await service.get_application_service(application_id)


@router.put("/{application_id}")
async def update_application(application_id: str, payload: ApplicationUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_application_service(application_id, update_data)
    return {"message": "updated"}


@router.delete("/{application_id}")
async def delete_application(application_id: str):
    await service.delete_application_service(application_id)
    return {"message": "deleted"}
