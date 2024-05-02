import datetime

from beanie import PydanticObjectId
from fastapi_users import schemas


class UserCreateDTO(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    birth_date: datetime.date


class UserBaseDTO(schemas.BaseUser[PydanticObjectId]):
    first_name: str
    last_name: str
    birth_date: datetime.date


class UserUpdateDTO(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
