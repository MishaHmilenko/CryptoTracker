import os
import asyncio
from dataclasses import dataclass

from beanie import init_beanie
from fastapi_users.db import BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.db.models.coin import Coin
from src.db.models.price_log import PriceLog
from src.db.models.tracking_crypto import TrackedCrypto
from src.db.models.user import User


@dataclass
class DBConfig:
    user = os.environ['MONGO_USER']
    password = os.environ['MONGO_PASSWORD']
    host = os.environ['MONGO_HOST']
    port = os.environ['MONGO_PORT']
    database = os.environ['MONGO_DB']
    replset = os.environ['MONGO_RS']

    @property
    def url(self):
        return f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?authSource=admin&replicaSet={self.replset}&w=majority'


class MongoDB:
    def __init__(self, config) -> None:
        self.config = config
        self.client = AsyncIOMotorClient(config.url, uuidRepresentation='standard')
        self.db = self.client.get_default_database()


async def initialize_beanie(db: AsyncIOMotorDatabase) -> None:
    await init_beanie(database=db, document_models=[User, Coin, PriceLog, TrackedCrypto])


def get_db(config) -> MongoDB:
    # params: config type DBConfig OR TestDBConfig

    return MongoDB(config)


async def get_db_user() -> BeanieUserDatabase:
    yield BeanieUserDatabase(User)

