from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from starlette.templating import Jinja2Templates

from src.db.models.user import User
from src.smtp.main import SmtpServer


def send_verify_mail(user: User, html_content: Jinja2Templates.TemplateResponse) -> None:
    smtp = SmtpServer()

    msg = MIMEMultipart()
    msg['From'] = 'admin@gmail.com'
    msg['To'] = user.email
    msg['Subject'] = 'Subject of the Email'

    msg.attach(MIMEText(html_content.body.decode(), 'html'))
    smtp.server.sendmail(from_addr='admin@gmail.com', to_addrs=user.email, msg=msg.as_string())
    smtp.server.close()
