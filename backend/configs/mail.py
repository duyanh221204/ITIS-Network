import smtplib
from email.mime.text import MIMEText

from utils.constants import Constant

SMTP_HOST = Constant.SMTP_HOST
SMTP_PORT = Constant.SMTP_PORT
SMTP_USERNAME = Constant.SMTP_USERNAME
SMTP_PASSWORD = Constant.SMTP_PASSWORD


def send_email(recipient: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = recipient

    with smtplib.SMTP_SSL(SMTP_HOST, int(SMTP_PORT)) as mail_server:
        mail_server.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail_server.sendmail(SMTP_USERNAME, [recipient], msg.as_string())
