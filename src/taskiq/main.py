from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker

from src.dishka.container import container
from src.db.main import get_db, initialize_beanie, DBConfig


class CustomListQueueBroker(ListQueueBroker):
    async def startup(self) -> None:
        await super().startup()
        await initialize_beanie(get_db(DBConfig()).db)
        setup_dishka_taskiq(container, broker)


broker = CustomListQueueBroker(
    url='redis://redis:6379',
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)]
)
