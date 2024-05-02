from src.db.models.user import User


class UserDAO:
    def __init__(self, collection):
        self.collection = collection

    async def update_value_of_verify(self, user: User):
        return await self.collection.update_one(
            {'user_id': user.id},
            {'$set': {'is_verified': True}}
        )
