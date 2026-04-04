from app.core.database import redis_client


async def get_cached(url: str) -> str | None:
    return await redis_client.get(f"scrape:{url}")


async def set_cached(url: str, content: str, ttl_seconds: int = 3600) -> None:
    await redis_client.set(f"scrape:{url}", content, ex=ttl_seconds)
