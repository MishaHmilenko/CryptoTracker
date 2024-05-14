from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from src.business_logic.user.main import UserBusinessLogicService
from src.db.models.user import User
from src.smtp.main import SmtpServer


class MsgDataModel(BaseModel):
    from_email: str
    to_email: str
    subject: str | None = None
    text: str | None = None
    html: str | None = None


def get_msg_object(msg_data: MsgDataModel) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['From'] = msg_data.from_email
    msg['To'] = msg_data.to_email
    msg['Subject'] = msg_data.subject

    if msg_data.text:
        msg.attach(MIMEText(msg_data.text, 'plain'))
    print('before attach html')
    if msg_data.html:
        msg.attach(MIMEText(msg_data.html, 'html'))
    print('after attach html')

    return msg


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


