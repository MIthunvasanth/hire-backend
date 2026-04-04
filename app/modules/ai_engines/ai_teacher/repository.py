from app.core.database import db

collection = db["teacher_sessions"]


async def create_session(data: dict) -> str:
    result = await collection.insert_one({**data, "status": "created"})
    return str(result.inserted_id)


async def list_sessions() -> list[dict]:
    items: list[dict] = []
    async for s in collection.find():
        items.append(s)
    return items
