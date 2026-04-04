from bson import ObjectId

from app.core.database import db

collection = db["resumes"]


async def create_resume(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_resume(resume_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(resume_id)})


async def get_all_resumes() -> list[dict]:
    items: list[dict] = []
    async for r in collection.find():
        items.append(r)
    return items


async def update_resume(resume_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(resume_id)}, {"$set": data})


async def delete_resume(resume_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(resume_id)})
