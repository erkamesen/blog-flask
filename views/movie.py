from flask import Blueprint, render_template, request, redirect, url_for
from controller import movie_deleter, movie_adder, movie_lister

movie = Blueprint("movie", __name__,
                  template_folder="../templates", static_folder="../static")


@movie.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":  
        return render_template("select.html", movie_datas = movie_lister())
    else:
        return render_template("add.html")


@movie.route("/added")
def added():
    movie_adder()
    return redirect(url_for("home.get_all_posts"))


@movie.route("/delete")
def delete_movie():
    movie_deleter(request.args.get("id"))
    return redirect(url_for("home.get_all_posts"))
