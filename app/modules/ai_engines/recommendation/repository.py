from bson import ObjectId

from app.core.database import db

collection = db["recommendations"]


async def create_recommendation(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_recommendation(recommendation_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(recommendation_id)})


async def get_all_recommendations() -> list[dict]:
    items: list[dict] = []
    async for r in collection.find():
        items.append(r)
    return items


async def update_recommendation(recommendation_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(recommendation_id)}, {"$set": data})


async def delete_recommendation(recommendation_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(recommendation_id)})
