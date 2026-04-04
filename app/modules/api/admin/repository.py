from bson import ObjectId

from app.core.database import db

collection = db["admins"]


async def create_admin(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_admin(admin_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(admin_id)})


async def get_all_admins() -> list[dict]:
    admins: list[dict] = []
    async for a in collection.find():
        admins.append(a)
    return admins


async def update_admin(admin_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(admin_id)}, {"$set": data})


async def delete_admin(admin_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(admin_id)})
