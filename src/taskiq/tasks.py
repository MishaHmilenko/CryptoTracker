import logging

from src.smtp.send_mail import send_mail_with_greeting
from src.taskiq.main import broker


@broker.task
async def best_task_ever():
    print('Best task ever1111111111111111111111111')
    logging.info('DO TASK')


@broker.task
async def send_greeting_every_morning(
    smtp='di', service='di'
):
    await send_mail_with_greeting(smtp, service)
