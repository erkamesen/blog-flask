from flask import Blueprint, render_template
from models import BlogPost, Movie, db
from flask_login import current_user
from datetime import datetime

bp = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")

@bp.route('/', methods=["GET", "POST"])
def get_all_posts():
    movies = Movie.query.order_by(Movie.rating).all()
    print("sa")
    print(movies)
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
        print(movies)
    db.session.commit()
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user, movies = movies)



