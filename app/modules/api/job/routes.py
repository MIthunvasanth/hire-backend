from fastapi import APIRouter

from .schema import JobCreate, JobUpdate
from . import service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
async def create_job(data: JobCreate):
    job_id = await service.create_job_service(data.model_dump())
    return {"id": job_id}


@router.get("/")
async def list_jobs():
    return await service.list_jobs_service()


@router.get("/{job_id}")
async def get_job(job_id: str):
    return await service.get_job_service(job_id)


@router.put("/{job_id}")
async def update_job(job_id: str, data: JobUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    await service.update_job_service(job_id, update_data)
    return {"message": "updated"}


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    await service.delete_job_service(job_id)
    return {"message": "deleted"}
