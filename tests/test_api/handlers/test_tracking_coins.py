import logging

import pytest
from httpx import AsyncClient

from src.business_logic.coin.dto import TrackingCoinDTO
from src.db.models.coin import Coin
from src.db.models.tracking_crypto import TrackedCrypto
from src.db.models.user import User

from tests.fixtures.client import client
from tests.fixtures.tracked_coin_fixtures import tracking_coin_data
from tests.fixtures.user_fixtures import current_user, registered_user, register_data, login_data, user_auth_token_data

logging.basicConfig(level=logging.INFO)


class TestTrackingCoinsHandlers:

    @pytest.mark.asyncio
    async def test_add_tracking_coin(
            self,
            client: AsyncClient,
            tracking_coin_data: TrackingCoinDTO,
            user_auth_token_data: dict,
    ):

        response = await client.post(
            'coins/start-tracking',
            json=tracking_coin_data.model_dump(),
            headers={
                'Authorization': f"{user_auth_token_data['token_type']} {user_auth_token_data['access_token']}"
            }
        )

        assert response.status_code == 200

        assert await Coin.find_one(Coin.slug == tracking_coin_data.slug) is not None
        assert await TrackedCrypto.find_one(TrackedCrypto.crypto.slug == tracking_coin_data.slug, fetch_links=True) is not None
