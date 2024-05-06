from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.api.stub import Stub

router = APIRouter(prefix='/user-templates', tags=['user-templates'])


@router.get('/verify-button/{token}')
async def verify_button(
        request: Request, token: str, templates: Annotated[Jinja2Templates, Depends(Stub(Jinja2Templates))]
):
    return templates.TemplateResponse(
        request=request,
        name="verify.html",
        context={"token": token}
    )
