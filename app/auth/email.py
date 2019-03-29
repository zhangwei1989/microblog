from flask import render_template, current_app
from flask_babel import _
from app.email import send_email
from config import Operations


def send_password_reset_email(user):
    token = user.get_jwt_token(operation=Operations.RESET_PASSWORD)
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_confirm_email(user):
    token = user.get_jwt_token(operation=Operations.CONFIRM)
    send_email(_('[Microblog] Eamil Confirm'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, token=token))