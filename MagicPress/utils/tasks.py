from .. import celery, mail
from flask_mail import Message
from flask import current_app

@celery.task(name='send_async_email')
def send_async_email(message_details):
    """Background task to send an email with Flask-Mail."""
    try:
        msg = Message(message_details['subject'],
                      message_details['recipients'])
        msg.body = message_details['body']
        mail.send(msg)
    except Exception as e:
        current_app.logger.info(e)
