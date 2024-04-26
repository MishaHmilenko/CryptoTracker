import logging
from typing import Annotated

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.controllers.main import setup_controllers
from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.db.main import mongo
from src.api.stub import Stub

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def factory_user_dao(db: Annotated[AsyncIOMotorDatabase, Depends(Stub(AsyncIOMotorDatabase))]) -> UserDAO:
    return UserDAO(collection=db.users)


def factory_user_logic_service(dao: Annotated[UserDAO, Depends(UserDAO)]) -> UserBusinessLogicService:
    return UserBusinessLogicService(dao=dao)


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo')

    setup_controllers(app)

    db = mongo.db

    app.dependency_overrides.update({
        Stub(AsyncIOMotorDatabase): lambda: db,
        Stub(UserDAO): factory_user_dao,
        Stub(UserBusinessLogicService): factory_user_logic_service,
    })

    return app
