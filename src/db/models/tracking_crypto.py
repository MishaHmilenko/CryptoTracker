from beanie import Document, Link

from src.db.models.coin import Coin
from src.db.models.user import User


class TrackedCrypto(Document):
    users: list[Link[User]]
    crypto: Link[Coin]
