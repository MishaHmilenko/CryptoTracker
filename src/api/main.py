from contextlib import asynccontextmanager
from typing import Annotated

from dishka.integrations.taskiq import setup_dishka
from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.controllers.main import setup_controllers
from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.api.stub import Stub
from src.db.main import get_db, initialize_beanie
from src.dishka.container import container
from src.smtp.main import SmtpServer, get_smtp_server
from src.taskiq.main import broker, redis_source
from src.taskiq.tasks import send_greeting_every_morning


def factory_smtp_server() -> SmtpServer:
    return SmtpServer()


def factory_user_dao(db: Annotated[AsyncIOMotorDatabase, Depends(Stub(AsyncIOMotorDatabase))]) -> UserDAO:
    return UserDAO()


def factory_user_logic_service(dao: Annotated[UserDAO, Depends(UserDAO)]) -> UserBusinessLogicService:
    return UserBusinessLogicService(dao=dao)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo = get_db()

    app.state.smtp = get_smtp_server()

    if not broker.is_worker_process:
        print("Starting broker")
        await broker.startup()

    await redis_source.startup()

    # await send_greeting_every_morning.schedule_by_cron(
    #     redis_source,
    #     '*/1 * * * *'
    # )

    await initialize_beanie(mongo.db)

    yield

    app.state.smtp.server.close()

    if not broker.is_worker_process:
        print('Shutting down broker')
        await broker.shutdown()

    await redis_source.shutdown()

    await container.close()


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo', lifespan=lifespan)

    setup_controllers(app)
    setup_dishka(container, broker)

    mongo = get_db()

    app.dependency_overrides.update({
        Stub(AsyncIOMotorDatabase): lambda: mongo.db,
        Stub(UserDAO): factory_user_dao,
        Stub(UserBusinessLogicService): factory_user_logic_service,
        Stub(SmtpServer): factory_smtp_server
    })

    return app
