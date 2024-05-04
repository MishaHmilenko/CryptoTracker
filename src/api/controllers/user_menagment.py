import asyncio

from beanie import PydanticObjectId
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users_db_beanie import ObjectIDIDMixin, BeanieUserDatabase
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from starlette.requests import Request

from src.api.controllers.utils_generate_template import generate_verify_template
from src.api.fastapi_bg_tasks.user_tasks import send_verify_mail
from src.db.main import get_db_user
from src.db.models.user import User

SECRET = 'SECRET'


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    verification_token_secret = SECRET

    async def on_after_register(
            self, user: User, request: Request | None = None
    ) -> None:
        print(f'User {user.id} has registered.')

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ) -> None:
        htm_content = generate_verify_template(user, token, request)
        await asyncio.to_thread(lambda: send_verify_mail(user, htm_content))


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_db_user)) -> UserManager:
    yield UserManager(user_db)


barer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=barer_transport,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
