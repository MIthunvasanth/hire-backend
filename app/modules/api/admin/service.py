from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_admin_service(data: dict) -> str:
    return await repository.create_admin(data)


async def get_admin_service(admin_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_admin(admin_id))


async def list_admins_service() -> list[dict]:
    items = await repository.get_all_admins()
    return [normalize_mongo_doc(i) for i in items]


async def update_admin_service(admin_id: str, data: dict) -> None:
    await repository.update_admin(admin_id, data)


async def delete_admin_service(admin_id: str) -> None:
    await repository.delete_admin(admin_id)
