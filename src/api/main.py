import logging
import os
import smtplib
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.api.controllers.main import setup_controllers
from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.api.stub import Stub
from src.db.main import get_db, initialize_beanie
from src.smtp.main import SmtpServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def factory_smtp_server() -> SmtpServer:
    return SmtpServer()


def factory_user_dao(db: Annotated[AsyncIOMotorDatabase, Depends(Stub(AsyncIOMotorDatabase))]) -> UserDAO:
    return UserDAO(collection=db.users)


def factory_user_logic_service(dao: Annotated[UserDAO, Depends(UserDAO)]) -> UserBusinessLogicService:
    return UserBusinessLogicService(dao=dao)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo = get_db()
    await initialize_beanie(mongo.db)
    yield


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo', lifespan=lifespan)

    setup_controllers(app)

    mongo = get_db()

    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.dependency_overrides.update({
        Stub(AsyncIOMotorDatabase): lambda: mongo.db,
        Stub(UserDAO): factory_user_dao,
        Stub(UserBusinessLogicService): factory_user_logic_service,
        Stub(SmtpServer): factory_smtp_server
    })

    return app
