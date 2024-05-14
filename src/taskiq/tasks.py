from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.business_logic.user.main import UserBusinessLogicService
from src.smtp.main import SmtpServer
from src.smtp.send_mail import send_mail_with_greeting
from src.taskiq.main import broker


@broker.task(schedule=[{'cron': '*/1 * * * *'}])
@inject
async def send_greeting_every_morning(
        smtp: FromDishka[SmtpServer], service: FromDishka[UserBusinessLogicService]
):
    # await send_mail_with_greeting(smtp, service)
    ...