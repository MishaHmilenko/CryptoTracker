import pytest_asyncio

from src.business_logic.coin.dto import TrackingCoinDTO
from src.db.models.coin import Coin


@pytest_asyncio.fixture(scope='function')
async def tracking_coin_data() -> TrackingCoinDTO:
    return TrackingCoinDTO(slug="bitcoin")


# @pytest_asyncio.fixture(scope='function')
# async def coin_in_db(tracking_coin_data: TrackingCoinDTO) -> Coin:
#     return await Coin.find_one(Coin.slug == tracking_coin_data.slug)

