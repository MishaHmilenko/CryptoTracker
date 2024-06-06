from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from tests.conftest import build_test_app


@pytest_asyncio.fixture(scope='function')
async def client() -> AsyncGenerator[AsyncClient, Any]:
    app = await build_test_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client

    app.state.mongo.db.User.delete_many({})
