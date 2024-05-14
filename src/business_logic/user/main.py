from src.db.dao.user_dao import UserDAO
from src.db.models.user import User


class UserBusinessLogicService:
    def __init__(self, dao: UserDAO) -> None:
        self._dao = dao

    async def get_emails(self) -> list[str]:
        return await self._dao.get_all_emails()


    async def add_new_field(self):
        return await self._dao.add_new_field()
