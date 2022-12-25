from flask import Blueprint, render_template
from controller import get_posts_and_movies


home = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")

@home.route('/', methods=["GET", "POST"])
def index():
    posts, movies = get_posts_and_movies() 
    return render_template("index.html", all_posts=posts, movies = movies)


