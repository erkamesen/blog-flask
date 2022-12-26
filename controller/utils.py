from functools import wraps
from flask import abort
from flask_login import current_user
from dotenv import load_dotenv
import os

from pkg.telegram import Logger
from pkg.mail_sender import MailSender


load_dotenv()

def mail_sender(message):
    
    logger = Logger(token=os.getenv("telegramApi"), chat_id=os.getenv("chatID"))
    sender = MailSender("erkamesen789@gmail.com", token=os.getenv("SMTPTOKEN"))
    logger.info(message)
    try:
        sender.send_message(message, os.getenv("MAIL_RECEIVER"))
    except UnicodeEncodeError:
        pass
        

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function














