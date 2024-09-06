from src.infrastructure.price_service.exceptions import KVPairNotFound
from src.temporary_storage.interface import TemporaryStorage


class TemporaryStorageService:
    def __init__(self, temporary_storage: TemporaryStorage):
        self.temporary_storage = temporary_storage

    async def get_value_from_record(self, name: str) -> str:
        try:
            return await self.temporary_storage.get(name)

        except KVPairNotFound:
            raise

    async def process_of_updating_value(self, name: str, value: str) -> None:
        value_of_record = await self.get_value_from_record(name)

        if value_of_record is None:
            await self.temporary_storage.set_value(name, float(value))
        elif float(value) > float(value_of_record):
            await self.temporary_storage.set_value(name, float(value))
