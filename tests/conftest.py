import os
from dataclasses import dataclass
from fastapi import FastAPI

from src.db.main import initialize_beanie, get_db

from src.api.controllers.main import setup_controllers


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


async def build_test_app() -> FastAPI:

    app = FastAPI(title='FastAPI Test App')

    setup_controllers(app)

    mongo = get_db(TestDBConfig())

    app.state.mongo = mongo

    await initialize_beanie(mongo.db)

    return app
