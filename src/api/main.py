import logging

from multiprocessing import Process

from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from fastapi import FastAPI

from src.api.controllers.main import setup_controllers
from src.db.main import get_db, initialize_beanie, DBConfig, run_second_process, watch_changes_in_coin_collection
from src.dishka.container import container
from src.smtp.main import get_smtp_server
from src.taskiq.main import broker
from src.db.dao.coin_dao import CoinDAO
from src.crypto_api.binance_websocket import CryptoWebsocket


@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo = get_db(DBConfig())

    await initialize_beanie(mongo.db)

    await broker.startup()

    app.state.smtp = get_smtp_server()

    mongo_stream_process = Process(target=run_second_process)
    mongo_stream_process.start()

    yield

    await broker.shutdown()

    await container.close()

    mongo_stream_process.terminate()
    mongo_stream_process.join()


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo', lifespan=lifespan)

    setup_controllers(app)

    # setup di
    setup_dishka_taskiq(container, broker)
    setup_dishka_fastapi(container, app)

    return app
