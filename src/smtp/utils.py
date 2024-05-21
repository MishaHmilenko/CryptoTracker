from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.smtp.models import MsgDataModel


def get_msg_object(msg_data: MsgDataModel) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['From'] = msg_data.from_email
    msg['To'] = msg_data.to_email
    msg['Subject'] = msg_data.subject

    if msg_data.text:
        msg.attach(MIMEText(msg_data.text, 'plain'))
    if msg_data.html:
        msg.attach(MIMEText(msg_data.html, 'html'))

    return msg
