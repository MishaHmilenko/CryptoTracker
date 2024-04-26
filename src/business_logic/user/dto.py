from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserBaseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr
