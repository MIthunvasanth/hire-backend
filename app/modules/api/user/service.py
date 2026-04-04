from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_user_service(data: dict) -> str:
    return await repository.create_user(data)


async def get_user_service(user_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_user(user_id))


async def list_users_service() -> list[dict]:
    users = await repository.get_all_users()
    return [normalize_mongo_doc(u) for u in users]


async def update_user_service(user_id: str, data: dict) -> None:
    await repository.update_user(user_id, data)


async def delete_user_service(user_id: str) -> None:
    await repository.delete_user(user_id)
