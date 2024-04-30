from flask import current_app, render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from threading import Thread
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email_confirmation(user):
    token = user.generate_confirmation_token()
    confirm_url = current_app.url_for('confirm_email', token=token, _external=True)
    msg = Message("Please confirm your email",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.html = render_template('activate.html', username=user.username, confirm_url=confirm_url)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.generate_reset_token()
    msg = Message('Reset Your Password',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[user.email])
    msg.html = render_template('password_reset_email.html', token=token, username=user.username)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()