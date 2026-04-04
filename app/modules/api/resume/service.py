from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_resume_service(data: dict) -> str:
    return await repository.create_resume(data)


async def get_resume_service(resume_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_resume(resume_id))


async def list_resumes_service() -> list[dict]:
    items = await repository.get_all_resumes()
    return [normalize_mongo_doc(i) for i in items]


async def update_resume_service(resume_id: str, data: dict) -> None:
    await repository.update_resume(resume_id, data)


async def delete_resume_service(resume_id: str) -> None:
    await repository.delete_resume(resume_id)
