from fastapi import APIRouter

from . import service
from .schema import RecruiterCreate, RecruiterUpdate

router = APIRouter(prefix="/recruiters", tags=["Recruiter"])


@router.post("/")
async def create_recruiter(payload: RecruiterCreate):
    recruiter_id = await service.create_recruiter_service(payload.model_dump())
    return {"id": recruiter_id}


@router.get("/")
async def list_recruiters():
    return await service.list_recruiters_service()


@router.get("/{recruiter_id}")
async def get_recruiter(recruiter_id: str):
    return await service.get_recruiter_service(recruiter_id)


@router.put("/{recruiter_id}")
async def update_recruiter(recruiter_id: str, payload: RecruiterUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_recruiter_service(recruiter_id, update_data)
    return {"message": "updated"}


@router.delete("/{recruiter_id}")
async def delete_recruiter(recruiter_id: str):
    await service.delete_recruiter_service(recruiter_id)
    return {"message": "deleted"}
