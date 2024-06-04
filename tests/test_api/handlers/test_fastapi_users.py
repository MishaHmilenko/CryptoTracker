import pytest


class TestUserHandlers:

    @pytest.mark.asyncio
    async def test_user_register(self, client, created_user):
        test_data = {
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "first_name": "string",
            "last_name": "string",
            "birth_date": "2024-05-29"
        }

        response = await client.post(
            'auth/jwt/register',
            json=test_data
        )

        assert response.json()['email'] == test_data['email']
        assert response.json()['first_name'] == test_data['first_name']
        assert response.json()['last_name'] == test_data['last_name']
        assert response.json()['birth_date'] == test_data['birth_date']

        assert created_user is not None

        assert response.status_code == 201

