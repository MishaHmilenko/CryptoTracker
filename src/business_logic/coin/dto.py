from bson import ObjectId
from pydantic import BaseModel


class TrackingCoinDTO(BaseModel):
    slug: str


class CoinCreateDTO(BaseModel):
    name: str
    symbol: str
    slug: str


class CoinBaseDTO(BaseModel):
    id: ObjectId
    name: str
    symbol: str
    slug: str

    class Config:
        arbitrary_types_allowed = True
