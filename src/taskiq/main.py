import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

redis_async_result = RedisAsyncResultBackend(
    redis_url='redis://redis:6379'
)

broker = ListQueueBroker(
    url='redis://redis:6379',
    result_backend=redis_async_result
)

redis_source = RedisScheduleSource('redis://redis:6379')

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[redis_source],
)

taskiq_fastapi.init(broker, 'src.api.main:build_app')
