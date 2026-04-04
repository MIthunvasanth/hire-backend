from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_session_service(data: dict) -> str:
    return await repository.create_session(data)


async def list_sessions_service() -> list[dict]:
    items = await repository.list_sessions()
    return [normalize_mongo_doc(i) for i in items]
