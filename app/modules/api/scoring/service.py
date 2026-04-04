from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_score_service(data: dict) -> str:
    return await repository.create_score(data)


async def get_score_service(score_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_score(score_id))


async def list_scores_service() -> list[dict]:
    items = await repository.get_all_scores()
    return [normalize_mongo_doc(i) for i in items]


async def update_score_service(score_id: str, data: dict) -> None:
    await repository.update_score(score_id, data)


async def delete_score_service(score_id: str) -> None:
    await repository.delete_score(score_id)
