from bson import ObjectId

from src.business_logic.coin.dto import CoinCreateDTO
from src.db.models.coin import Coin


class CoinDAO:

    def __init__(self):
        self.collection = Coin

    async def get_coin_by_id(self, coin_id: ObjectId) -> Coin:
        return await self.collection.find_one({"_id": coin_id})

    async def get_coin_by_slug(self, slug: str) -> Coin:
        return await self.collection.find_one({"slug": slug})

    async def get_all_coins(self) -> list[Coin]:
        return await self.collection.find().to_list()

    async def add_coin(self, coin_data: CoinCreateDTO) -> Coin:

        coin = Coin(
            name=coin_data.name,
            symbol=coin_data.symbol,
            slug=coin_data.slug,
        )

        await self.collection.insert_one(coin)

        return coin
