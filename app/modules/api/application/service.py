from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_application_service(data: dict) -> str:
    return await repository.create_application(data)


async def get_application_service(application_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_application(application_id))


async def list_applications_service() -> list[dict]:
    items = await repository.get_all_applications()
    return [normalize_mongo_doc(i) for i in items]


async def update_application_service(application_id: str, data: dict) -> None:
    await repository.update_application(application_id, data)


async def delete_application_service(application_id: str) -> None:
    await repository.delete_application(application_id)
