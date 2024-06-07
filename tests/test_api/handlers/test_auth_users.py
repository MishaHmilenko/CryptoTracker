from datetime import datetime

import pytest
from httpx import AsyncClient

from src.db.models.user import User

from tests.fixtures.client import client
from tests.fixtures.user_fixtures import (register_data, login_data, created_user, registered_user,
                                          request_verify_token_data, request_verify_data, token_verify)


class TestUserHandlers:

    @pytest.mark.asyncio
    async def test_user_register(
            self, client: AsyncClient, register_data: dict, created_user: User
    ):
        response = await client.post(
            'auth/jwt/register',
            json=register_data
        )

        assert response.json()['email'] == register_data['email']
        assert response.json()['first_name'] == register_data['first_name']
        assert response.json()['last_name'] == register_data['last_name']
        assert response.json()['birth_date'] == register_data['birth_date']

        assert created_user is not None

        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_user_register_already_exists(
            self,
            client: AsyncClient,
            registered_user: User,  # Create user
            register_data: dict
    ):

        # Try to create user again
        response = await client.post(
            url='auth/jwt/register',
            json=register_data
        )

        assert response.status_code == 400

        assert response.json()['detail'] == 'REGISTER_USER_ALREADY_EXISTS'

    @pytest.mark.asyncio
    async def test_user_register_invalid_data(
        self, client: AsyncClient
    ):
        response = await client.post(
            url='auth/jwt/register',
            json={}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_user_login(
            self,
            client: AsyncClient,
            registered_user: User,
            login_data: dict
    ):

        response = await client.post(
            'auth/jwt/login',
            data=login_data
        )

        assert response.status_code == 200, f'Login failed": {response.json()}'

        assert 'access_token' in response.json()
        assert response.json()['token_type'] == 'bearer'

    @pytest.mark.asyncio
    async def test_user_login_bad_credentials(
            self,
            client: AsyncClient,
            registered_user: User,
            login_data: dict
    ):
        login_data['password'] = 'bad_password'

        response = await client.post(
            'auth/jwt/login',
            data=login_data
        )

        assert response.status_code == 400

        assert response.json()['detail'] == 'LOGIN_BAD_CREDENTIALS'

    @pytest.mark.asyncio
    async def test_user_login_invalid_data(
            self,
            client: AsyncClient,
            registered_user: User
    ):
        response = await client.post(
            'auth/jwt/login',
            data={}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_user_request_verify_token(
            self,
            client: AsyncClient,
            request_verify_token_data: dict
    ):
        response = await client.post(
            'auth/request-verify-token',
            json=request_verify_token_data
        )

        assert response.status_code == 202

    @pytest.mark.asyncio
    async def test_user_request_verify_token_invalid_data(
            self,
            client: AsyncClient,
            request_verify_token_data: dict
    ):
        response = await client.post(
            'auth/request-verify-token',
            json={}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_user_verify(
            self, client: AsyncClient, registered_user: User, token_verify: str, request_verify_data: dict
    ):
        response = await client.post(
            'auth/verify',
            json=request_verify_data
        )

        assert response.status_code == 200

        assert response.json()['email'] == registered_user.email
        assert response.json()['first_name'] == registered_user.first_name
        assert response.json()['last_name'] == registered_user.last_name
        assert datetime.strptime(response.json()['birth_date'], '%Y-%m-%d').date() == registered_user.birth_date

        assert response.json()['is_verified'] is True

    @pytest.mark.asyncio
    async def test_user_verify_bad_token(
            self,
            client: AsyncClient
    ):

        verify_bad_data = {
            'token': 'bad_token'
        }

        response = await client.post(
            'auth/verify',
            json=verify_bad_data
        )

        assert response.status_code == 400

        assert response.json()['detail'] == 'VERIFY_USER_BAD_TOKEN'

    @pytest.mark.asyncio
    async def test_user_verify_invalid_data(
            self,
            client: AsyncClient
    ):
        response = await client.post(
            'auth/verify',
            json={}
        )

        assert response.status_code == 422
