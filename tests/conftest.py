import logging
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import FastAPI

from src.db.main import initialize_beanie, get_db

from beanie import init_beanie

from src.api.controllers.main import setup_controllers
from src.db.models.user import User


@dataclass
class TestDBConfig:
    user = os.environ['MONGO_TEST_USER']
    password = os.environ['MONGO_TEST_PASSWORD']
    host = os.environ['MONGO_TEST_HOST']
    port = os.environ['MONGO_TEST_PORT']
    database = os.environ['MONGO_TEST_DB']

    @property
    def url(self):
        print('TEST database', self.database)
        print('TEST PORT', self.port)
        return f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?authSource=admin'


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    mongo = get_db(TestDBConfig())

    await init_beanie(database=mongo.db, document_models=[User])

    yield


def build_test_app() -> FastAPI:
    print('START BUILD TEST APP')
    logging.info('START BUILD TEST APP')

    app = FastAPI(title='FastAPI Test App', lifespan=test_lifespan)

    setup_controllers(app)

    return app
