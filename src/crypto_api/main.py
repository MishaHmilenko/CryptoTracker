import logging
import os

import requests

from src.business_logic.coin.dto import CoinCreateDTO
from src.business_logic.coin.exceptions import CoinNotFoundInAPI


class CryptoApiService:

    def __init__(self):
        self.base_info_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': os.environ['COIN_API_KEY'],
        }

    def _make_request(self, url: str, headers: dict, params: dict) -> requests.Response:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
        except requests.RequestException:
            raise CoinNotFoundInAPI()

        return response

    async def get_coin_by_slug(self, slug) -> CoinCreateDTO:
        params = {'slug': slug}

        response = self._make_request(url=self.base_info_url, headers=self.headers, params=params)

        data = response.json()

        coin_info = data['data'][next(iter(data['data']))]

        return CoinCreateDTO(
            name=coin_info['name'],
            symbol=coin_info['symbol'],
            slug=coin_info['slug'],
        )
