import os

from redis.asyncio import from_url

from src.temporary_storage.interface import TemporaryStorage


class RedisStorage(TemporaryStorage):

    def __init__(self) -> None:
        self.redis = from_url(f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}?decode_responses=True')

    async def get(self, name: str):
        return await self.redis.get(name=name)

    async def set_value(self, name: str, value: float) -> bool:
        return await self.redis.set(name=name, value=value)
