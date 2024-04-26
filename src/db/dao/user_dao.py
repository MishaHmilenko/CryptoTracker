from bson import ObjectId

from src.business_logic.user.dto import UserCreateDTO
from src.business_logic.user.auth_utils import hash_password, validate_password


class UserDAO:
    def __init__(self, collection):
        self.collection = collection

    async def create_user(self, user: UserCreateDTO):
        user.password = hash_password(user.password)
        user = await self.collection.insert_one(user.dict())
        return user.inserted_id

    async def get_user_by_id(self, user_id) -> dict:
        return await self.collection.find_one({'_id': ObjectId(user_id)})

    async def get_user_by_email(self, email) -> dict:
        return await self.collection.find_one({'email': email})

    async def get_all_users(self) -> list[dict]:
        return await self.collection.find().to_list(length=100)


