import json

import websockets


class BinanceWebsocket:

    def __init__(self, crypto_trade_streams):

        self.crypro_trade_streams = crypto_trade_streams
        self.base_url = 'wss://fstream.binance.com/stream'

        self.websocket = None
        self.running = True

    async def connect_to_trade_websocket(self):
        uri = f'{self.base_url}?streams={self.crypro_trade_streams}'

        async with websockets.connect(uri) as websocket:
            self.websocket = websocket

            await self.handle_messages()

    async def handle_messages(self):

        while self.running:
            try:
                message = await self.websocket.recv()
                print('Message of socket', json.loads(message))
            except websockets.ConnectionClosed:
                print('Connection closed')
                break

    async def stop_connection(self):
        self.running = False

        if self.websocket:
            await self.websocket.close()
            print('Websocket closed')


async def get_binance_websocket():
    return BinanceWebsocket('btcusdt@aggTrade/ethusdt@aggTrade')
