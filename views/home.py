from flask import Blueprint, render_template
from models import BlogPost
from flask_login import current_user
from datetime import datetime

bp = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")

@bp.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)

