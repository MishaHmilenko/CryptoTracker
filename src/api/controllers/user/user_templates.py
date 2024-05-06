from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.db.models.user import User

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