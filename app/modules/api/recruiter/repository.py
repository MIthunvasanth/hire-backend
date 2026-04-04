from bson import ObjectId

from app.core.database import db

collection = db["recruiters"]


async def create_recruiter(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_recruiter(recruiter_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(recruiter_id)})


async def get_all_recruiters() -> list[dict]:
    recruiters: list[dict] = []
    async for r in collection.find():
        recruiters.append(r)
    return recruiters


async def update_recruiter(recruiter_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(recruiter_id)}, {"$set": data})


async def delete_recruiter(recruiter_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(recruiter_id)})
