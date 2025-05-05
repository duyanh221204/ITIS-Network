import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(recipient: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient

    with smtplib.SMTP_SSL(SMTP_HOST, int(SMTP_PORT)) as mail_server:
        mail_server.login(SMTP_USER, SMTP_PASSWORD)
        mail_server.sendmail(SMTP_USER, [recipient], msg.as_string())
