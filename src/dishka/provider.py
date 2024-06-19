from dishka import Provider, provide, Scope

from src.business_logic.coin.logic import CoinBusinessLogicService
from src.business_logic.user.logic import UserBusinessLogicService
from src.crypto_api.main import CryptoApiService
from src.db.dao.coin_dao import CoinDAO
from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.db.dao.user_dao import UserDAO
from src.smtp.main import SmtpServer


class DishkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_user_dao(self) -> UserDAO:
        return UserDAO()

    @provide(scope=Scope.APP)
    def get_user_service(self, dao: UserDAO) -> UserBusinessLogicService:
        return UserBusinessLogicService(dao=dao)

    @provide(scope=Scope.APP)
    async def get_coin_dao(self) -> CoinDAO:
        return CoinDAO()

    @provide(scope=Scope.APP)
    async def get_crypto_api_service(self) -> CryptoApiService:
        return CryptoApiService()

    @provide(scope=Scope.APP)
    async def get_tracking_dao(self) -> CryptoTrackingDAO:
        return CryptoTrackingDAO()

    @provide(scope=Scope.APP)
    async def get_coin_service(
            self,
            coin_dao: CoinDAO,
            tracked_dao: CryptoTrackingDAO,
            crypto_api_service: CryptoApiService
    ) -> CoinBusinessLogicService:

        return CoinBusinessLogicService(
            coin_dao=coin_dao,
            tracked_dao=tracked_dao,
            crypto_api_service=crypto_api_service
        )

    @provide(scope=Scope.APP)
    def get_smtp(self) -> SmtpServer:
        return SmtpServer()


provider = DishkaProvider()
