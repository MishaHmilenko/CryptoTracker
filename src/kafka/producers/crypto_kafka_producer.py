import json
import os

from aiokafka import AIOKafkaProducer


class CryptoKafkaProducer:

    def __init__(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f'{os.getenv("KAFKA_BROKER_HOST")}:{os.getenv("KAFKA_BROKER_PORT")}',
            value_serializer=lambda msg: json.dumps(msg).encode('utf-8')
        )

    async def start_producer(self) -> None:
        await self.producer.start()

    async def send_msg_to_topic(self, msg: dict) -> None:
        await self.producer.send(topic='Crypto', value=msg)

    async def stop_producer(self) -> None:
        await self.producer.stop()

