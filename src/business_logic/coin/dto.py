from pydantic import BaseModel


class TrackingCoin(BaseModel):
    slug: str


class CoinCreate(BaseModel):
    name: str
    symbol: str
    slug: str
