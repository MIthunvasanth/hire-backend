from fastapi import APIRouter

from . import service
from .schema import ResumeCreate, ResumeUpdate

router = APIRouter(prefix="/resumes", tags=["Resume"])


@router.post("/")
async def create_resume(payload: ResumeCreate):
    resume_id = await service.create_resume_service(payload.model_dump())
    return {"id": resume_id}


@router.get("/")
async def list_resumes():
    return await service.list_resumes_service()


@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    return await service.get_resume_service(resume_id)


@router.put("/{resume_id}")
async def update_resume(resume_id: str, payload: ResumeUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_resume_service(resume_id, update_data)
    return {"message": "updated"}


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    await service.delete_resume_service(resume_id)
    return {"message": "deleted"}
