from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.params import Depends

from src.api.controllers.user.user_menagment import current_active_user
from src.business_logic.coin.dto import TrackingCoinDTO
from src.business_logic.coin.logic import CoinBusinessLogicService
from src.business_logic.user.dto import UserBaseDTO
from src.db.models.user import User

router = APIRouter(prefix='/coins', tags=['Coins'])


@router.post('/start-tracking')
@inject
async def start_tracking(
        coin_data: TrackingCoinDTO,
        service: FromDishka[CoinBusinessLogicService],
        user: User = Depends(current_active_user),
):
    await service.add_tracking(coin_data, UserBaseDTO.from_orm(user))


@router.post('/stop-tracking')
@inject
async def stop_tracking(
        coin_data: TrackingCoinDTO,
        service: FromDishka[CoinBusinessLogicService],
        user: User = Depends(current_active_user)
):
    await service.stop_tracking(coin_data, UserBaseDTO.from_orm(user))
