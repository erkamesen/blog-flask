from flask import Flask, render_template, redirect, url_for, flash, abort, request
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user, UserMixin
from forms import LoginForm, RegisterForm, CreatePostForm, CommentForm
from datetime import datetime
import requests
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import LoginManager




from views.home import home
from views.user import user
from views.movie import movie
from views.admin import admin

from models import db, User, BlogPost, Comment

app = Flask(__name__)
app.config.from_pyfile("config.py")

### PACKAGES ###

bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro',
                    force_default=False, force_lower=False, use_ssl=False, base_url=None)

db.init_app(app)

app.register_blueprint(user)
app.register_blueprint(home)
app.register_blueprint(movie)
app.register_blueprint(admin)

@app.context_processor
def quotes():
    response = requests.get("https://zenquotes.io/api/random")
    quotes = response.json()[0]["q"]
    quotes_owner = response.json()[0]["a"]
    return {'quotes': quotes, "quotes_owner": quotes_owner}

@app.context_processor
def copyright_date():
    return {'now': datetime.utcnow()}

@app.context_processor
def month_name():
    return {'month': date.today().strftime("%B")}




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



""" with app.app_context():
    db.drop_all()
    db.create_all()  """

if __name__ == "__main__":
    app.run()
