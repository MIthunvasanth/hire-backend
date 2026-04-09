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


async def get_gap_analyses_for_user(user_id: str | None, user_email: str | None, limit: int = 30) -> list[dict]:
    query_parts: list[dict] = []
    if user_id:
        query_parts.append({"user_id": user_id})
        query_parts.append({"candidate_id": user_id})

    if user_email:
        normalized_email = user_email.lower()
        query_parts.append({"user_email": normalized_email})
        query_parts.append({"candidate_id": normalized_email})

    if not query_parts:
        return []

    query = {"$or": query_parts}

    items: list[dict] = []
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    async for g in cursor:
        items.append(g)
    return items


async def update_gap_analysis(gap_analysis_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(gap_analysis_id)}, {"$set": data})


async def delete_gap_analysis(gap_analysis_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(gap_analysis_id)})
