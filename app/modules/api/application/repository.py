from bson import ObjectId

from app.core.database import db

collection = db["applications"]


async def create_application(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_application(application_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(application_id)})


async def get_all_applications() -> list[dict]:
    items: list[dict] = []
    async for a in collection.find():
        items.append(a)
    return items


async def update_application(application_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(application_id)}, {"$set": data})


async def delete_application(application_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(application_id)})
