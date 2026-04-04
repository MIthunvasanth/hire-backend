from bson import ObjectId

from app.core.database import db

collection = db["users"]


async def create_user(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_user(user_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(user_id)})


async def get_all_users() -> list[dict]:
    users: list[dict] = []
    async for user in collection.find():
        users.append(user)
    return users


async def update_user(user_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})


async def delete_user(user_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(user_id)})
