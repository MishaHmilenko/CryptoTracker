from src.api.controllers.user.user_menagment import CurrentUser
from src.business_logic.coin.dto import TrackingCoin
from src.crypto_api.main import CryptoApiService
from src.db.dao.coin_dao import CoinDAO
from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.db.models.user import User


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

    async def add_tracking(self, tracking_coin_data: TrackingCoin, user: User):

        if await self._coin_dao.get_coin_by_slug(tracking_coin_data.slug):
            return

        coin_data = await self.crypto_api_service.get_coin_by_slug(tracking_coin_data.slug)
        await self._coin_dao.add_coin(coin_data)
        await self._tracked_dao.add_tracking(user, coin_data) # тут надо передавать объект монеты

        return {'detail': 'Coin added'}



