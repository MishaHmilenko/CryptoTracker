from beanie import Document


class Coin(Document):
    name: str
    symbol: str
    slug: str
