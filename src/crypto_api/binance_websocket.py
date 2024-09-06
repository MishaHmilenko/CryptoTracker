import asyncio
import json

import websockets
from websockets import WebSocketClientProtocol

from src.db.dao.tracking_crypto_dao import CryptoTrackingDAO
from src.kafka.producers.crypto_kafka_producer import CryptoKafkaProducer


class CryptoWebsocket:

    def __init__(self, crypto_tracking_dao: CryptoTrackingDAO, kafka_producer: CryptoKafkaProducer) -> None:
        self.base_url = 'wss://fstream.binance.com/stream'

        self.connection_to_trade_streams: WebSocketClientProtocol | None = None

        self._crypto_tracking_dao = crypto_tracking_dao
        self._kafka_producer = kafka_producer

        self.task_listen_trade_stream: asyncio.Task | None = None

    async def connect_to_trade_streams(self, uri: str) -> None:
        self.connection_to_trade_streams = await websockets.connect(uri)

    async def disconnect_from_trade_streams(self) -> None:
        if self.connection_to_trade_streams:
            await self.connection_to_trade_streams.close()

    async def format_coins_to_path_params(self) -> str:
        list_of_coins = await self._crypto_tracking_dao.get_coins_witch_users_track()

        list_of_params = [f'{coin.symbol.lower()}usdt@aggTrade/' for coin in list_of_coins]

        return ''.join(list_of_params).rstrip('/')

    async def receive_message(self) -> str | None:
        if self.connection_to_trade_streams:
            return await self.connection_to_trade_streams.recv()

    async def listen_trade_streams(self) -> None:
        params = await self.format_coins_to_path_params()

        uri = f'{self.base_url}?streams={params}'

        try:
            await self.connect_to_trade_streams(uri)

            while True:
                data_ws_msg = json.loads(await self.receive_message())['data']

                await self._kafka_producer.send_msg_to_topic(
                    msg={'symbol': data_ws_msg['s'], 'price': data_ws_msg['p']}
                )

        except asyncio.CancelledError:
            raise

        except websockets.ConnectionClosed:
            raise

        finally:
            await self.disconnect_from_trade_streams()

    async def start_listening(self) -> None:
        await self._kafka_producer.start_producer()

        if self.task_listen_trade_stream:
            self.task_listen_trade_stream.cancel()

        self.task_listen_trade_stream = asyncio.create_task(self.listen_trade_streams())


async def get_crypto_websocket() -> CryptoWebsocket:
    return CryptoWebsocket(crypto_tracking_dao=CryptoTrackingDAO(), kafka_producer=CryptoKafkaProducer())
