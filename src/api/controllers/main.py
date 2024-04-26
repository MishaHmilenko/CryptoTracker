from src.api.controllers.user import router as user_router


def setup_controllers(app) -> None:
    app.include_router(user_router)
