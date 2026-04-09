from app.core.database import db

collection = db["parsed_resumes"]
ats_collection = db["parsed_resume_ats"]


async def create_parsed_resume(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_latest_parsed_resume(user_id: str | None, user_email: str | None) -> dict | None:
    query: dict = {}
    if user_id:
        query["user_id"] = user_id
    elif user_email:
        query["user_email"] = user_email.lower()

    if not query:
        return None

    return await collection.find_one(query, sort=[("created_at", -1)])


async def get_parsed_resume_by_id(resume_id: str) -> dict | None:
    from bson import ObjectId

    return await collection.find_one({"_id": ObjectId(resume_id)})


async def create_ats_result(data: dict) -> str:
    result = await ats_collection.insert_one(data)
    return str(result.inserted_id)


async def get_latest_ats_result(user_id: str | None, user_email: str | None) -> dict | None:
    query: dict = {}
    if user_id:
        query["user_id"] = user_id
    elif user_email:
        query["user_email"] = user_email.lower()

    if not query:
        return None

    return await ats_collection.find_one(query, sort=[("created_at", -1)])