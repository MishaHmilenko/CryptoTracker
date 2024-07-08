import asyncio
import websockets
import streamlit

from src.db.dao.coin_dao import CoinDAO

class BinanceWebsocket:

    def __init__(self, coin_dao: CoinDAO):
        self.base_url = 'wss://fstream.binance.com/stream'

        self.connection_to_trade_streams = None

        self.coin_dao = coin_dao


    async def connect_to_trade_streams(self, crypto_trade_streams: str):
        self.connection_to_trade_streams = await websockets.connect(crypto_trade_streams)

    async def disconnect_from_trade_streams(self):
        if self.connection_to_trade_streams:
            await self.connection_to_trade_streams.close()

    async def format_coins_to_path_params(self) -> str:
        print('Enter123123312133213312321321123')
        list_of_coins = await self.coin_dao.get_all_coins()
        print('EXITQEQEREQEREQR')
        print('List of coins: ', list_of_coins)

        list_of_params = [f'{coin.symbol.lower()}usdt@aggTrade/' for coin in list_of_coins]
        print('List of params for coin ws', list_of_params)

        return ''.join(list_of_params)


    async def receive_message(self):
        if self.connection_to_trade_streams:
            return await self.connection_to_trade_streams.recv()

    async def listen_trade_streams(self):

        params = await self.format_coins_to_path_params()

        uri = f'{self.base_url}?streams={params}'

        print('URI ', uri)

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
    ws_process = Process(target=run_binance_websocket)
    ws_process.start()
    ws_process.join()
    # asyncio.run(run_binance_websocket())
    # ws = BinanceWebsocket(coin_dao)
    # streamlit.session_state.event_loop = asyncio.new_event_loop()
    # streamlit.session_state.event_loop.run_until_complete(ws.listen_trade_streams())

