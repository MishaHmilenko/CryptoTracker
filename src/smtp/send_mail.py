from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from starlette.templating import Jinja2Templates

from src.business_logic.user.main import UserBusinessLogicService
from src.db.models.user import User
from src.smtp.main import SmtpServer
from src.smtp.models import MsgDataModel
from src.smtp.utils import get_msg_object


def send_verify_mail(
        user: User,
        html_content: Jinja2Templates.TemplateResponse,
        smtp: SmtpServer
) -> None:
    msg = MIMEMultipart()
    msg['From'] = 'admin@gmail.com'
    msg['To'] = user.email
    msg['Subject'] = 'Subject of the Email'

    msg.attach(MIMEText(html_content.body.decode(), 'html'))
    smtp.server.sendmail(from_addr='admin@gmail.com', to_addrs=user.email, msg=msg.as_string())


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


