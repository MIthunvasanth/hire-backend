import logging

from app.core.database import db
from app.core.database import redis_client


logger = logging.getLogger(__name__)
collection = db["scraped_jobs"]


async def get_cached(url: str) -> str | None:
    try:
        return await redis_client.get(f"scrape:{url}")
    except Exception as exc:
        logger.warning("scraper cache read skipped: redis unavailable (%s)", exc)
        return None


async def set_cached(url: str, content: str, ttl_seconds: int = 3600) -> None:
    try:
        await redis_client.set(f"scrape:{url}", content, ex=ttl_seconds)
    except Exception as exc:
        logger.warning("scraper cache write skipped: redis unavailable (%s)", exc)


async def create_scrape_record(data: dict) -> str:
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def list_user_scrape_records(user_id: str | None, user_email: str | None, limit: int = 25) -> list[dict]:
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
