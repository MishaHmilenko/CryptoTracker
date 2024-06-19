from typing import Any

from fastapi import HTTPException


class CoinNotFound(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Coin not found',
            headers=headers
        )

class CoinAlreadyExists(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Coin already exists',
            headers=headers
        )

class UserAlreadyTracksCoin(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='User already tracks this coin',
            headers=headers
        )