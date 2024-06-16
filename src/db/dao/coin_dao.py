from src.business_logic.coin.dto import CoinCreate
from src.db.models.coin import Coin


class CoinDAO:

    def __init__(self):
        self.collection = Coin

    async def add_coin(self, coin_data: CoinCreate) -> None:

        coin = Coin(
            name=coin_data.name,
            symbol=coin_data.symbol,
            slug=coin_data.slug,
        )

        await self.collection.insert_one(coin)

    async def get_coin_by_slug(self, slug: str) -> Coin:
        return await self.collection.find_one({"slug": slug})
