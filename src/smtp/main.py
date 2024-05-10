import os
import smtplib


class SmtpServer:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])


def get_smtp_server() -> SmtpServer:
    return SmtpServer()
