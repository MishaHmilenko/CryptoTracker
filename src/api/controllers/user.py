from typing import Annotated

from fastapi import APIRouter, Depends

from src.business_logic.user.dto import UserBaseDTO, UserCreateDTO
from src.business_logic.user.main import UserBusinessLogicService
from src.api.stub import Stub

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create', response_model=UserBaseDTO)
async def create_user(
        user: UserCreateDTO, service: Annotated[UserBusinessLogicService, Depends(Stub(UserBusinessLogicService))]
):
    return await service.create_user(user)


@router.get('/get/{user_id}', response_model=UserBaseDTO)
async def get_user(
        user_id: str, service: Annotated[UserBusinessLogicService, Depends(Stub(UserBusinessLogicService))]
):
    return await service.get_user(user_id)


@router.get('/all', response_model=list[UserBaseDTO])
async def get_users(
        service: Annotated[UserBusinessLogicService, Depends(Stub(UserBusinessLogicService))]
):
    return await service.get_users()
