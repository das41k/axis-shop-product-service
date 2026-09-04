from redis.asyncio import Redis
from .config import settings

class RedisManager:
    def __init__(self):
        self.redis: Redis | None = None
    
    async def connect(self):
        self.redis = Redis.from_url(
            settings.REDIS_URL,
            decode_responses = True,
            encoding = "utf-8"
        )
        await self.redis.ping()
    
    async def close(self):
        if self.redis:
            await self.redis.aclose()
            
redis_manager = RedisManager()