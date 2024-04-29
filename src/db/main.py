import os
from dataclasses import dataclass

from beanie import init_beanie
from fastapi_users.db import BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.db.models.user import User


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
        self.client = AsyncIOMotorClient(config.url, uuidRepresentation='standard')
        self.db = self.client.get_default_database()


async def initialize_beanie(db: AsyncIOMotorDatabase):
    await init_beanie(database=db, document_models=[User])


def get_db():
    return MongoDB(DBConfig())


async def get_db_user() -> BeanieUserDatabase:
    yield BeanieUserDatabase(User)
