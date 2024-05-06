from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.db.models.user import User


def generate_verify_template(user: User, token: str, request: Request) -> Jinja2Templates.TemplateResponse:
    templates = Jinja2Templates(directory="static/templates")
    return templates.TemplateResponse(
        request=request,
        name="mail.html",
        context={"user": user, "token": token}
    )

