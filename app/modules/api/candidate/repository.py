from bson import ObjectId

from app.core.database import db

collection = db["candidates"]


async def create_candidate(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_candidate(candidate_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(candidate_id)})


async def get_all_candidates() -> list[dict]:
    candidates: list[dict] = []
    async for c in collection.find():
        candidates.append(c)
    return candidates


async def update_candidate(candidate_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(candidate_id)}, {"$set": data})


async def delete_candidate(candidate_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(candidate_id)})
