from src.business_logic.user.dto import UserCreateDTO, UserBaseDTO
from src.db.dao.user_dao import UserDAO

from fastapi import HTTPException


class UserBusinessLogicService:
    def __init__(self, dao: UserDAO) -> None:
        self._dao = dao

    async def create_user(self, user_data: UserCreateDTO):

        if await self._dao.get_user_by_email(user_data.email) is not None:
            raise HTTPException(status_code=400, detail="User already registered")

        user_id = await self._dao.create_user(user_data)
        user = await self._dao.get_user_by_id(user_id)
        return UserBaseDTO(id=str(user['_id']), name=user['name'], email=user['email'])

    async def get_user(self, user_id) -> UserBaseDTO:
        user = await self._dao.get_user_by_id(user_id)
        return UserBaseDTO(id=str(user["_id"]), name=user["name"], email=user["email"])

    async def get_users(self) -> list[UserBaseDTO]:
        users = await self._dao.get_all_users()
        return [
            UserBaseDTO(id=str(user["_id"]), name=user["name"], email=user["email"])
            for user in users
        ]
