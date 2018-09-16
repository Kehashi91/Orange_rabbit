from flask import current_app
from flask_mail import Message
from threading import Thread
from orabbit import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, text_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender="mail.orangerabbit@gmail.com", recipients=["mail.orangerabbit@gmail.com"])
    msg.body = text_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()