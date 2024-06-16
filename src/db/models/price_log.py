from datetime import datetime

from beanie import Document, Link

from src.db.models.coin import Coin


class PriceLog(Document):
    coin: Link[Coin]
    price: float
    date: datetime = datetime.now()
