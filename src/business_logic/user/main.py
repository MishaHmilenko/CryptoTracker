from src.db.dao.user_dao import UserDAO
from src.db.models.user import User


class UserBusinessLogicService:
    def __init__(self, dao: UserDAO) -> None:
        self._dao = dao

    async def verify_user(self, user: User):
        return await self._dao.update_value_of_verify(user)
