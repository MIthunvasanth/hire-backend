from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_recruiter_service(data: dict) -> str:
    return await repository.create_recruiter(data)


async def get_recruiter_service(recruiter_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_recruiter(recruiter_id))


async def list_recruiters_service() -> list[dict]:
    items = await repository.get_all_recruiters()
    return [normalize_mongo_doc(i) for i in items]


async def update_recruiter_service(recruiter_id: str, data: dict) -> None:
    await repository.update_recruiter(recruiter_id, data)


async def delete_recruiter_service(recruiter_id: str) -> None:
    await repository.delete_recruiter(recruiter_id)
