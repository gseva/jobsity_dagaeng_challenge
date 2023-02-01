
import os
import smtplib

from email.message import EmailMessage

EMAIL_MESSAGE = '''
Hi there!

I'm the trips API and I wanted to let you know that the ingestion finished successfully.
{} rows were inserted!

Cheers
'''

def send_email(rows):
    host = os.environ.get('SMTP_HOST')
    port = os.environ.get('SMTP_PORT')
    username = os.environ.get('SMTP_USERNAME')
    password = os.environ.get('SMTP_PASSWORD')

    msg = EmailMessage()
    msg.set_content(EMAIL_MESSAGE.format(rows))
    msg['Subject'] = 'Trips API: ingestion successful'
    msg['From'] = os.environ.get('EMAIL_SENDER')
    msg['To'] = os.environ.get('EMAIL_RECIPIENT')

    s = smtplib.SMTP_SSL(host, port)
    s.login(username, password)
    s.send_message(msg)
    s.quit()
