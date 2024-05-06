from src.api.controllers.user_menagment import fastapi_users, auth_backend
from src.business_logic.user.dto import UserBaseDTO, UserCreateDTO, UserUpdateDTO
from src.api.controllers.user_templates import router as user_templates_router


def setup_controllers(app) -> None:
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix='/auth/jwt',
        tags=['auth']
    )

    app.include_router(
        fastapi_users.get_register_router(UserBaseDTO, UserCreateDTO),
        prefix='/auth/jwt',
        tags=['auth']
    )

    app.include_router(
        fastapi_users.get_users_router(UserBaseDTO, UserUpdateDTO),
        prefix='/users',
        tags=['users'],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserBaseDTO),
        prefix='/auth',
        tags=['auth']
    )

    app.include_router(user_templates_router)
