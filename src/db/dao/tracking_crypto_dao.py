from src.db.models.coin import Coin
from src.db.models.tracking_crypto import TrackedCrypto
from src.db.models.user import User


class CryptoTrackingDAO:

    def __init__(self):
        self.collection = TrackedCrypto

    async def add_tracking(self, user: User, coin: Coin):
        print('start add tracking in crypto tracking dao')
        tracked_crypto = TrackedCrypto(users=[user], crypto=coin)

        await self.collection.insert_one(self.collection(tracked_crypto))

