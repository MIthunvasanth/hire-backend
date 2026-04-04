from app.core.database import db


async def counts() -> dict:
    users = await db["users"].count_documents({})
    candidates = await db["candidates"].count_documents({})
    jobs = await db["jobs"].count_documents({})
    applications = await db["applications"].count_documents({})

    return {
        "users": users,
        "candidates": candidates,
        "jobs": jobs,
        "applications": applications,
    }
