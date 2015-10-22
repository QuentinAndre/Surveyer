from flask import render_template
from flask.ext.mail import Message
from Surveyer import mail
from instance.config import MAIL_USERNAME


def send_email(subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipient)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password(user, token):
    send_email("Your password reset request.", user.email, [MAIL_USERNAME],
               render_template('mails/reset_password.txt', user=user, token=token),
               render_template('mails/reset_password.html', user=user, token=token))
