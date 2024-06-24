from typing import Any

from fastapi import HTTPException


class CoinNotFoundInAPI(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Coin not found in crypto API service',
            headers=headers
        )


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
            status_code=403,
            detail='Coin already exists',
            headers=headers
        )


class TrackingNotFound(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=404,
            detail='Tracking not found by this coin',
            headers=headers
        )


class UserNotTrackCoin(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=400,
            detail='User doesn\'t track the coin',
            headers=headers
        )


class UserAlreadyTracksCoin(HTTPException):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            status_code=403,
            detail='User already tracks this coin',
            headers=headers
        )