import pytest
import pytest_asyncio
from beanie.odm.queries.find import FindOne
from httpx import AsyncClient

from src.db.models.user import User

from tests.fixtures.client import client

from fastapi_users.jwt import generate_jwt, SecretType


verification_token_audience: str = 'fastapi-users:verify'

verification_token_secret: SecretType = 'SECRET'
verification_token_lifetime_seconds: int = 3600


@pytest_asyncio.fixture(scope='function')
async def register_data() -> dict:
    return {
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
        "first_name": "string",
        "last_name": "string",
        "birth_date": "2024-05-29"
    }


@pytest_asyncio.fixture(scope='function')
async def registered_user(client: AsyncClient, register_data: dict) -> User:

    await client.post(
        'auth/jwt/register',
        json=register_data
    )

    user = await User.find_one(User.email == 'user@example.com')

    return user


@pytest_asyncio.fixture(scope='function')
async def login_data() -> dict:
    return {
            "username": "user@example.com",
            "password": "string"
        }


@pytest.fixture(scope='function')
def created_user() -> FindOne[User]:
    return User.find_one(User.email == 'user@example.com')


@pytest_asyncio.fixture(scope='function')
async def request_verify_token_data() -> dict:
    return {
        "email": "user@example.com"
    }


@pytest_asyncio.fixture(scope='function')
async def token_verify(client: AsyncClient, registered_user: User) -> str:
    token_data = {
        'sub': str(registered_user.id),
        'email': registered_user.email,
        'aud': verification_token_audience
    }

    token = generate_jwt(
        token_data,
        verification_token_secret,
        verification_token_lifetime_seconds,
    )

    return token


@pytest_asyncio.fixture(scope='function')
async def request_verify_data(token_verify: str):
    return {
        'token': token_verify
    }
