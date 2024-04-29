from beanie import PydanticObjectId
from fastapi_users import schemas


class UserCreateDTO(schemas.BaseUserCreate):
    pass


class UserBaseDTO(schemas.BaseUser[PydanticObjectId]):
    pass


class UserUpdateDTO(schemas.BaseUserUpdate):
    pass
