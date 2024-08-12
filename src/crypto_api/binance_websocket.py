import websockets

from src.db.dao.coin_dao import CoinDAO


class CryptoWebsocket:

    def __init__(self, coin_dao: CoinDAO):
        self.base_url = 'wss://fstream.binance.com/stream'

        self.connection_to_trade_streams = None

        self._coin_dao = coin_dao

    async def connect_to_trade_streams(self, crypto_trade_streams_uri: str):
        self.connection_to_trade_streams = await websockets.connect(crypto_trade_streams_uri)

    async def disconnect_from_trade_streams(self):
        if self.connection_to_trade_streams:
            await self.connection_to_trade_streams.close()

    async def format_coins_to_path_params(self) -> str:
        list_of_coins = await self._coin_dao.get_all_coins()

        list_of_params = [f'{coin.symbol.lower()}usdt@aggTrade/' for coin in list_of_coins]

        return ''.join(list_of_params)[:-1]

    async def receive_message(self):
        if self.connection_to_trade_streams:
            return await self.connection_to_trade_streams.recv()

    async def listen_trade_streams(self):
        params = await self.format_coins_to_path_params()

        uri = f'{self.base_url}?streams={params}'

        try:
            await self.connect_to_trade_streams(uri)

            while True:
                message = await self.receive_message()

        except websockets.ConnectionClosed:
            pass

        finally:
            await self.disconnect_from_trade_streams()


async def start_listen_trade_streams():
    ws = CryptoWebsocket(CoinDAO())
    await ws.listen_trade_streams()
