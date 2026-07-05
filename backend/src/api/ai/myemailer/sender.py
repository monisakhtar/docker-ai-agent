from curses.ascii import EM
import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "notset")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "notset")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "notset")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "465"))

def send_email(subject: str, content: str, to_email: str):
    if EMAIL_ADDRESS == "notset" or EMAIL_PASSWORD == "notset":
        raise ValueError("Email credentials are not set in environment variables.")

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)