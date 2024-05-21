from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from fastapi import FastAPI

from src.api.controllers.main import setup_controllers
from src.db.main import get_db, initialize_beanie
from src.dishka.container import container
from src.taskiq.main import broker


@asynccontextmanager
async def lifespan(app: FastAPI):

    await initialize_beanie(get_db().db)

    await broker.startup()

    yield

    await broker.shutdown()

    await container.close()


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo', lifespan=lifespan)

    setup_controllers(app)

    # setup di
    setup_dishka_taskiq(container, broker)
    setup_dishka_fastapi(container, app)

    return app
