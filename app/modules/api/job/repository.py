from bson import ObjectId

from app.core.database import db

collection = db["jobs"]


async def create_job(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def get_job(job_id: str) -> dict | None:
    return await collection.find_one({"_id": ObjectId(job_id)})


async def get_all_jobs() -> list[dict]:
    jobs: list[dict] = []
    async for job in collection.find():
        jobs.append(job)
    return jobs


async def update_job(job_id: str, data: dict) -> None:
    await collection.update_one({"_id": ObjectId(job_id)}, {"$set": data})


async def delete_job(job_id: str) -> None:
    await collection.delete_one({"_id": ObjectId(job_id)})
