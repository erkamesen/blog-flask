from flask import Blueprint, render_template
from models import BlogPost, Movie, db
from flask_login import current_user
from datetime import datetime, date
from pkg.telegram import Logger
from controller import get_posts_and_movies

home = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")

@home.route('/', methods=["GET", "POST"])
def get_all_posts():  
    posts, movies = get_posts_and_movies() 
    return render_template("index.html", all_posts=posts, movies = movies)


