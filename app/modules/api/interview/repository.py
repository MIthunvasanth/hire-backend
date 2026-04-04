from bson import ObjectId

from app.core.database import db

collection = db["interviews"]


async def create_interview(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_interview(interview_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(interview_id)})


async def get_all_interviews() -> list[dict]:
    items: list[dict] = []
    async for i in collection.find():
        items.append(i)
    return items


async def update_interview(interview_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(interview_id)}, {"$set": data})


async def delete_interview(interview_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(interview_id)})
