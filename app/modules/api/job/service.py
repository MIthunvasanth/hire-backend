from . import repository
from app.utils.helpers import normalize_mongo_doc


async def create_job_service(data: dict) -> str:
    return await repository.create_job(data)


async def get_job_service(job_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_job(job_id))


async def list_jobs_service() -> list[dict]:
    jobs = await repository.get_all_jobs()
    return [normalize_mongo_doc(j) for j in jobs]


async def update_job_service(job_id: str, data: dict) -> None:
    await repository.update_job(job_id, data)


async def delete_job_service(job_id: str) -> None:
    await repository.delete_job(job_id)
