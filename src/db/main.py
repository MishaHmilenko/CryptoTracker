import os
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class DBConfig:
    user = os.environ['MONGO_USER']
    password = os.environ['MONGO_PASSWORD']
    host = os.environ['MONGO_HOST']
    port = os.environ['MONGO_PORT']
    database = os.environ['MONGO_DB']

    @property
    def url(self):
        return f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?authSource=admin'


class MongoDB:
    def __init__(self, config: DBConfig):
        self.client = AsyncIOMotorClient(config.url)
        self.db = self.client.get_default_database()


mongo = MongoDB(DBConfig())
