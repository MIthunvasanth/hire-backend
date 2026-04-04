from bson import ObjectId

from app.core.database import db

collection = db["scores"]


async def create_score(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_score(score_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(score_id)})


async def get_all_scores() -> list[dict]:
    items: list[dict] = []
    async for s in collection.find():
        items.append(s)
    return items


async def update_score(score_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(score_id)}, {"$set": data})


async def delete_score(score_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(score_id)})
