from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

from app.core.config import settings

mongo_client = AsyncIOMotorClient(settings.mongo_url)
db = mongo_client[settings.mongo_db_name]

redis_client = redis.from_url(settings.redis_url)
