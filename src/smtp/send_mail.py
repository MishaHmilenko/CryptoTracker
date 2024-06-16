from starlette.templating import Jinja2Templates

from src.business_logic.user.logic import UserBusinessLogicService
from src.db.models.user import User
from src.smtp.main import SmtpServer
from src.smtp.models import MsgDataModel
from src.smtp.utils import get_msg_object


def send_verify_mail(
        user: User,
        html_content: Jinja2Templates.TemplateResponse,
        smtp: SmtpServer
) -> None:

    msg_data = MsgDataModel(
        from_email='admin@gmail.com',
        to_email=user.email,
        html=html_content.body.decode(),
    )

    smtp.server.sendmail(
        from_addr='admin@gmail.com',
        to_addrs=user.email,
        msg=get_msg_object(msg_data).as_string()
    )


async def send_mail_with_greeting(
        smtp: SmtpServer, service: UserBusinessLogicService
) -> None:

    msg_data = MsgDataModel(
        from_email='admin@gmail.com',
        to_email=','.join(await service.get_emails()),
        subject='Greetings from Mongo App',
        text='Good morning!',
    )

    smtp.server.sendmail(
        from_addr='admin@gmail.com',
        to_addrs=await service.get_emails(),
        msg=get_msg_object(msg_data).as_string()
    )


