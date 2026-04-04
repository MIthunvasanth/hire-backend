from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_candidate_service(data: dict) -> str:
    return await repository.create_candidate(data)


async def get_candidate_service(candidate_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_candidate(candidate_id))


async def list_candidates_service() -> list[dict]:
    items = await repository.get_all_candidates()
    return [normalize_mongo_doc(i) for i in items]


async def update_candidate_service(candidate_id: str, data: dict) -> None:
    await repository.update_candidate(candidate_id, data)


async def delete_candidate_service(candidate_id: str) -> None:
    await repository.delete_candidate(candidate_id)
