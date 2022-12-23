from flask import Blueprint, render_template
from models import BlogPost, Movie, db
from flask_login import current_user
from datetime import datetime, date


home = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")

@home.route('/', methods=["GET", "POST"])
def get_all_posts():
    movies = Movie.query.order_by(Movie.rating).all()
    db.session.commit()
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user, movies = movies)


