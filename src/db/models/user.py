import datetime

from beanie import Document
from fastapi_users.db import BeanieBaseUser


class User(BeanieBaseUser, Document):
    first_name: str
    last_name: str
    birth_date: datetime.date
