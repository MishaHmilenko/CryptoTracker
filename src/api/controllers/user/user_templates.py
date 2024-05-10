# from dishka import FromDishka
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.business_logic.user.main import UserBusinessLogicService
from src.db.models.user import User
from src.dishka.provider import Obj
from src.smtp.main import SmtpServer
from src.taskiq.tasks import best_task_ever

router = APIRouter(prefix='/user-templates', tags=['user-templates'])
templates = Jinja2Templates(directory="static/templates")


@router.get('/verify-button/{token}')
async def verify_button(
        request: Request, token: str
):
    return templates.TemplateResponse(
        request=request,
        name="verify.html",
        context={"token": token}
    )


def generate_mail_template(user: User, token: str, request: Request) -> Jinja2Templates.TemplateResponse:
    return templates.TemplateResponse(
        request=request,
        name="mail.html",
        context={"user": user, "token": token}
    )


class MyVal(BaseModel):
    key: str
    val: str


@router.get('/best-task-ever')
async def get_best_task():
    await best_task_ever.kiq()


# @router.get('/test-dishka')
# @inject
# async def get_test_dishka(smtp: FromDishka[SmtpServer], obj: FromDishka[Obj]):
#     result = smtp()
#     return {'smtp': result, 'obj': obj.a}
