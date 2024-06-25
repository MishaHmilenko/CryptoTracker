from src.business_logic.coin.dto import TrackingCoinDTO, CoinCreateDTO, CoinBaseDTO
from src.business_logic.user.dto import UserBaseDTO
from src.crypto_api.main import CryptoApiService
from src.db.dao.coin_dao import CoinDAO
from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.db.dao.user_dao import UserDAO

from src.business_logic.coin.exceptions import CoinAlreadyExists, UserAlreadyTracksCoin, CoinNotFound, \
    TrackingNotFound, UserNotTrackCoin


class CoinBusinessLogicService:

    def __init__(
            self,
            coin_dao: CoinDAO,
            tracking_dao: CryptoTrackingDAO,
            user_dao: UserDAO,
            crypto_api_service: CryptoApiService
    ) -> None:

        self._coin_dao = coin_dao
        self._tracking_dao = tracking_dao
        self._user_dao = user_dao
        self.crypto_api_service = crypto_api_service

    async def create_coin(self, coin_data: CoinCreateDTO) -> CoinBaseDTO:

        if await self._coin_dao.get_coin_by_slug(coin_data.slug):
            raise CoinAlreadyExists()

        coin = await self._coin_dao.add_coin(coin_data)

        return CoinBaseDTO(
            id=coin.id,
            name=coin.name,
            symbol=coin.symbol,
            slug=coin.slug
        )

    async def get_coin_by_tracking_coin_data(self, tracking_coin_data: TrackingCoinDTO) -> CoinBaseDTO:

        coin = await self._coin_dao.get_coin_by_slug(tracking_coin_data.slug)

        if coin is None:
            raise CoinNotFound()

        return CoinBaseDTO(
            id=coin.id,
            name=coin.name,
            symbol=coin.symbol,
            slug=coin.slug
        )

    async def get_tracking_by_coin_data(self, coin_data: CoinBaseDTO) -> TrackingCoinDTO:

        tracking = await self._tracking_dao.get_tracking_by_coin_slug(coin_data.slug)

        if tracking is None:
            raise TrackingNotFound()

        return TrackingCoinDTO(
            slug=coin_data.slug
        )

    async def check_user_tracked_coin(self, user: UserBaseDTO, coin_data: CoinBaseDTO) -> bool:

        user_in_db = await self._user_dao.get_user_by_id(user.id)
        coin_in_db = await self._coin_dao.get_coin_by_id(coin_data.id)

        if user_in_db not in await self._tracking_dao.get_users_of_tracking_coin(coin_in_db):
            raise UserNotTrackCoin()

        return True

    async def create_tracking(self, coin_data: CoinBaseDTO, user: UserBaseDTO) -> None:

        await self._tracking_dao.add_coin_to_tracking(
            await self._coin_dao.get_coin_by_id(coin_data.id),
            await self._user_dao.get_user_by_id(user.id)
        )

    async def add_user_to_tracking(self, coin_data: CoinBaseDTO, user: UserBaseDTO) -> None:

        user_in_db = await self._user_dao.get_user_by_id(user.id)
        coin = await self._coin_dao.get_coin_by_id(coin_data.id)

        if user_in_db in await self._tracking_dao.get_users_of_tracking_coin(coin):
            raise UserAlreadyTracksCoin()

        await self._tracking_dao.add_user_to_tracking_coin(coin, user_in_db)

    async def add_tracking(self, tracking_coin_data: TrackingCoinDTO, user: UserBaseDTO) -> None:

        try:

            coin_in_db = await self.get_coin_by_tracking_coin_data(tracking_coin_data)

            if await self._tracking_dao.get_tracking_by_coin_slug(coin_in_db.slug):
                return await self.add_user_to_tracking(coin_in_db, user)
            else:
                return await self.create_tracking(coin_in_db, user)

        except CoinNotFound:

            coin_api_data = await self.crypto_api_service.get_coin_by_slug(tracking_coin_data.slug)

            coin = await self.create_coin(coin_api_data)
            await self.create_tracking(coin, user)

    async def stop_tracking(self, tracking_coin_data: TrackingCoinDTO, user: UserBaseDTO) -> None:
        try:
            coin_data = await self.get_coin_by_tracking_coin_data(tracking_coin_data)

            await self.get_tracking_by_coin_data(coin_data)

            await self.check_user_tracked_coin(user, coin_data)

            await self._tracking_dao.remove_user_of_tracking_coin(
                await self._coin_dao.get_coin_by_id(coin_data.id),
                await self._user_dao.get_user_by_id(user.id)
            )

        except (CoinNotFound, TrackingNotFound, UserNotTrackCoin):
            raise
