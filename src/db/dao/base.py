from motor.motor_asyncio import AsyncIOMotorCollection


class BaseDAO:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection
