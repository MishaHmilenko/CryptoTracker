import json
import os

from aiokafka import AIOKafkaConsumer

from src.infrastructure.price_service.logic import TemporaryStorageService
from src.temporary_storage.redis_storage import RedisStorage


class CryptoKafkaConsumer:

    def __init__(self, temporary_storage_service: TemporaryStorageService) -> None:
        self.consumer = AIOKafkaConsumer(
            'Crypto',
            bootstrap_servers=f'{os.getenv("KAFKA_BROKER_HOST")}:{os.getenv("KAFKA_BROKER_PORT")}',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda msg: json.loads(msg.decode('utf-8'))
        )
        self.temporary_storage_service = temporary_storage_service

    async def consuming_process(self) -> None:
        await self.consumer.start()

        try:
            while True:
                msg = await self.consumer.getone()

                await self.temporary_storage_service.process_of_updating_value(
                    name=msg.value['symbol'],
                    value=msg.value['price']
                )

        finally:
            await self.consumer.stop()


def get_crypto_kafka_consumer():
    return CryptoKafkaConsumer(TemporaryStorageService(temporary_storage=RedisStorage()))
