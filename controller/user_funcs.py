from forms import ContactForm
from controller import mail_sender
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import Comment, User
from werkzeug.security import generate_password_hash

# -*- coding: utf-8 -*-


def contact_me():
    form = ContactForm()
    form_name = form.name.data
    form_email = form.email.data
    form_text = form.text.data

    message = "Name: {}\nEmail: {}\nContent: {}".format(form_name, form_email, form_text)
    mail = MIMEMultipart('alternative')
    mail = MIMEText(message, 'html', 'UTF-8')        
    mail = mail.as_string()
    mail_sender(mail)
    
    
def new_comment(text, comment_author, parent_post):
    comment = Comment()
    comment.text = text
    comment.comment_author = comment_author
    comment.parent_post = parent_post
    comment.add_comment()
    
    
def new_user(password, email, name):
    
    hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
    new_user = User(
            email= email,
            name = name,
            password=hashed_password,
        )
    new_user.add_user()   
