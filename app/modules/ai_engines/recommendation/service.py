from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_recommendation_service(data: dict) -> str:
    return await repository.create_recommendation(data)


async def get_recommendation_service(recommendation_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_recommendation(recommendation_id))


async def list_recommendations_service() -> list[dict]:
    items = await repository.get_all_recommendations()
    return [normalize_mongo_doc(i) for i in items]


async def update_recommendation_service(recommendation_id: str, data: dict) -> None:
    await repository.update_recommendation(recommendation_id, data)


async def delete_recommendation_service(recommendation_id: str) -> None:
    await repository.delete_recommendation(recommendation_id)
