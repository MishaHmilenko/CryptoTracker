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

from src.crypto_api.binance_websocket import start_listen_trade_streams


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


async def watch_changes_in_coin_collection(db: AsyncIOMotorDatabase) -> None:

    pipeline = [{'$match': {}}]
    collection = db['Coin']

    async with collection.watch(pipeline=pipeline) as change_stream:
        while change_stream.alive:
            change = await change_stream.try_next()
            print(123, flush=True)

            if change is not None:
                asyncio.create_task(start_listen_trade_streams())
                continue

            await asyncio.sleep(5)


async def is_coin_collection_empty(db: AsyncIOMotorDatabase) -> bool:
    return True if await db['Coin'].count_documents(filter={}) == 0 else False


def run_second_process():
    mongo = get_db(DBConfig())

    event_loop = asyncio.get_event_loop()

    event_loop.run_until_complete(initialize_beanie(mongo.db))

    if not event_loop.run_until_complete(is_coin_collection_empty(mongo.db)):
        event_loop.create_task(start_listen_trade_streams())

    event_loop.run_until_complete(watch_changes_in_coin_collection(db=mongo.db))
