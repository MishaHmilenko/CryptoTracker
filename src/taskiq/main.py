import taskiq_fastapi
from redis import ConnectionPool
from starlette.requests import Request
from taskiq import TaskiqDepends
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

redis_async_result = RedisAsyncResultBackend(
    redis_url='redis://redis:6379'
)


broker = ListQueueBroker(
    url='redis://redis:6379',
    result_backend=redis_async_result
)


taskiq_fastapi.init(broker, 'src.api.main:build_app')


def get_redis_pool(request: Request = TaskiqDepends()) -> ConnectionPool:
    return request.app.state.redis_pool
