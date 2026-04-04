from app.core.database import db

collection = db["users"]


async def get_user_by_email(email: str) -> dict | None:
    return await collection.find_one({"email": email})


async def create_user(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)
