from bson import ObjectId

from app.core.database import db

collection = db["gap_analyses"]


async def create_gap_analysis(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_gap_analysis(gap_analysis_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(gap_analysis_id)})


async def get_all_gap_analyses() -> list[dict]:
    items: list[dict] = []
    async for g in collection.find():
        items.append(g)
    return items


async def update_gap_analysis(gap_analysis_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(gap_analysis_id)}, {"$set": data})


async def delete_gap_analysis(gap_analysis_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(gap_analysis_id)})
