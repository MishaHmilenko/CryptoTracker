import asyncio
import websockets

from src.business_logic.coin.logic import CoinBusinessLogicService


class BinanceWebsocket:

    def __init__(self, coin_logic_service: CoinBusinessLogicService):
        self.base_url = 'wss://fstream.binance.com/stream'

        self.connection_to_trade_streams = None

        self.coin_logic_service = coin_logic_service

    async def connect_to_trade_streams(self, crypto_trade_streams: str):
        self.connection_to_trade_streams = await websockets.connect(crypto_trade_streams)

    async def disconnect_from_trade_streams(self):
        if self.connection_to_trade_streams:
            await self.connection_to_trade_streams.close()

    async def receive_message(self):
        if self.connection_to_trade_streams:
            return await self.connection_to_trade_streams.recv()

    async def listen_trade_streams(self):
        print('Coin Logic Service', self.coin_logic_service)

        uri = f'{self.base_url}?streams='

        try:
            await self.connect_to_trade_streams(uri)

            while True:
                message = await self.receive_message()
                print(message)

        except websockets.ConnectionClosed:
            pass

        finally:
            await self.disconnect_from_trade_streams()


if __name__ == '__main__':
    ws = BinanceWebsocket()
    asyncio.run(ws.listen_trade_streams())

