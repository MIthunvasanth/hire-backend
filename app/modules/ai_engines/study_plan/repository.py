from bson import ObjectId

from app.core.database import db

collection = db["study_plans"]


async def create_study_plan(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_study_plan(plan_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(plan_id)})


async def list_study_plans_for_user(user_id: str | None, user_email: str | None, limit: int = 30) -> list[dict]:
    query_parts: list[dict] = []
    if user_id:
        query_parts.append({"user_id": user_id})

    if user_email:
        query_parts.append({"user_email": user_email.lower()})

    if not query_parts:
        return []

    query = {"$or": query_parts}

    items: list[dict] = []
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    async for item in cursor:
        items.append(item)
    return items


async def update_field_completion(plan_id: str, field_path: str, completed: bool) -> bool:
    result = await collection.update_one(
        {"_id": ObjectId(plan_id)},
        {"$set": {field_path: completed}},
    )
    return result.modified_count > 0


async def update_task_completion(plan_id: str, day_index: int, task_index: int, completed: bool) -> bool:
    return await update_field_completion(plan_id, f"plan.{day_index}.tasks.{task_index}.completed", completed)
