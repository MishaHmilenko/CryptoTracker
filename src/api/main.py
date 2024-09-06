import asyncio
from multiprocessing import Process

from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from fastapi import FastAPI

from src.api.controllers.main import setup_controllers
from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.db.main import get_db, initialize_beanie, DBConfig
from src.db.stream_coin_collection import run_coin_streaming_process
from src.dishka.container import container
from src.kafka.consumers.crypto_kafka_consumer import get_crypto_kafka_consumer
from src.kafka.kafka_admin import KafkaAdminClientService
from src.smtp.main import get_smtp_server
from src.taskiq.main import broker


@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo = get_db(DBConfig())

    await initialize_beanie(mongo.db)

    await broker.startup()

    app.state.smtp = get_smtp_server()

    KafkaAdminClientService().add_topic('Crypto')
    asyncio.create_task(get_crypto_kafka_consumer().consuming_process())

    coin_streaming_process = Process(target=run_coin_streaming_process)
    coin_streaming_process.start()

    yield

    await broker.shutdown()

    await container.close()

    coin_streaming_process.terminate()
    coin_streaming_process.join()


def build_app() -> FastAPI:
    app = FastAPI(title='CRUD_mongo', lifespan=lifespan)

    setup_controllers(app)

    # setup di
    setup_dishka_taskiq(container, broker)
    setup_dishka_fastapi(container, app)

    return app
