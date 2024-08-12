import asyncio

from motor.motor_asyncio import AsyncIOMotorDatabase

from src.crypto_api.binance_websocket import start_listen_trade_streams
from src.db.main import get_db, DBConfig, initialize_beanie


class CoinCollectionStream:

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db['Coin']

    async def watch_changes_in_coin_collection(self) -> None:
        pipeline = [{'$match': {}}]

        async with self.collection.watch(pipeline=pipeline) as change_stream:
            while change_stream.alive:
                change = await change_stream.try_next()

                if change is not None:
                    asyncio.create_task(start_listen_trade_streams())
                    continue

                await asyncio.sleep(1)

    async def is_coin_collection_empty(self) -> bool:
        return True if await self.collection.count_documents(filter={}) == 0 else False

    async def run_coin_streaming(self):

        if not await self.is_coin_collection_empty():
            asyncio.create_task(start_listen_trade_streams())

        await self.watch_changes_in_coin_collection()


def run_coin_streaming_process():
    mongo_db = get_db(DBConfig()).db

    event_loop = asyncio.get_event_loop()

    event_loop.run_until_complete(initialize_beanie(db=mongo_db))

    coin_stream = CoinCollectionStream(db=mongo_db)

    event_loop.run_until_complete(coin_stream.run_coin_streaming())
