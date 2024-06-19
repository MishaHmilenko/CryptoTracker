from src.business_logic.coin.dto import TrackingCoin, CoinCreate
from src.crypto_api.main import CryptoApiService
from src.db.dao.coin_dao import CoinDAO
from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.db.models.user import User
from src.db.models.coin import Coin


class CoinBusinessLogicService:

    def __init__(
            self,
            coin_dao: CoinDAO,
            tracked_dao: CryptoTrackingDAO,
            crypto_api_service: CryptoApiService
    ) -> None:

        self._coin_dao = coin_dao
        self._tracked_dao = tracked_dao
        self.crypto_api_service = crypto_api_service

    async def create_coin(self, coin_data: CoinCreate) -> Coin:

        if await self._coin_dao.get_coin_by_slug(coin_data.slug):
            raise CoinAlreadyExists()

        return self._coin_dao.add_coin(coin_data)

    async def create_tracking(self, coin: Coin, user: User) -> None:

        await self._tracked_dao.add_coin_to_tracking(coin, user)

    async def add_user_to_tracking(self, coin: Coin, user: User) -> None:

        if user in await self._tracked_dao.get_users_of_tracking_coin(coin):
            raise UserAlreadyTracksCoin()

        await self._tracked_dao.add_user_to_tracking_coin(coin, user)

    async def add_tracking(self, tracking_coin_data: TrackingCoin, user: User) -> None:

        coin_in_db = await self._coin_dao.get_coin_by_slug(tracking_coin_data.slug)

        if coin_in_db:

            if await self._tracked_dao.get_tracking_by_coin(coin_in_db):
                return await self.add_user_to_tracking(coin_in_db, user)
            else:
                return await self.create_tracking(coin_in_db, user)

        coin_api_data = await self.crypto_api_service.get_coin_by_slug(tracking_coin_data.slug)

        coin = await self.create_coin(coin_api_data)
        await self.create_tracking(coin, user)
