from jinja2 import Template
from flask import current_app as app
from flask import render_template

import os
import smtplib
from json import dumps

from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --------------

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@bloglite.v2.com"
SENDER_PASSWORD = ''


# getting PATHS
# --------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

DAILY_REMINDER_HTML_PATH = os.path.join(TEMPLATE_DIR, 'dailyReminder.html')
EXPORT_NOTIFICATION_HTML_PATH = os.path.join(TEMPLATE_DIR, 'exportNotification.html')


# -----------------
# handling MAILS.

def mail(user_mail, subject, message, content="text", attachment_files=None):

    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = user_mail
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_files:
        for file in attachment_files:
            with open(file, 'rb') as attachment:

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')

            encoders.encode_base64(part)
            msg.attach(part)

    server = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)

    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    return 'Mail Sent successfully !!'


# ---------------------------------------------------

# DAILY reminders.
# -----------------

def dailyReminderEmail(name, email): 
    with open(DAILY_REMINDER_HTML_PATH) as f:
        template = Template(f.read())
        message = template.render(name=name)

    today = datetime.today().strftime('%d-%m-%Y')
    subject = f'BLOGLITE-v2 : Daily Reminder Mail for ({today})'

    mail(email, subject=subject, message=message, content='html')

# dailyReminderEmail("Faizan", 'faizan@bloglite.com')






