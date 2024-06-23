from src.db.models.coin import Coin
from src.db.models.tracking_crypto import TrackedCrypto
from src.db.models.user import User


class CryptoTrackingDAO:

    def __init__(self):
        self.collection = TrackedCrypto

    async def add_coin_to_tracking(self, coin: Coin, user: User) -> None:
        tracked_crypto = self.collection(users=[user], crypto=coin)

        await self.collection.insert_one(tracked_crypto)

    async def get_users_of_tracking_coin(self, coin: Coin) -> list[User]:
        track_coin = await self.collection.find_one(self.collection.crypto.id == coin.id, fetch_links=True)
        return track_coin.users

    async def add_user_to_tracking_coin(self, coin: Coin, user: User) -> None:
        track_coin = await self.collection.find_one(self.collection.crypto.id == coin.id, fetch_links=True)
        track_coin.users.append(user)

        await self.collection.save(track_coin)

    async def remove_user_of_tracking_coin(self, coin: Coin, user: User) -> None:
        track_coin = await self.collection.find_one(self.collection.crypto.id == coin.id, fetch_links=True)
        track_coin.users.remove(user)

        await self.collection.save(track_coin)

    async def get_tracking_by_coin_slug(self, tracking_coin_slug: str) -> TrackedCrypto:
        return await self.collection.find_one(self.collection.crypto.slug == tracking_coin_slug, fetch_links=True)
