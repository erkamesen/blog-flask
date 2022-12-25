from flask import Blueprint, render_template, request, redirect, url_for
from controller.movie_funcs import save_movie, select_movie, movie_deleter

movie = Blueprint("movie", __name__,
                  template_folder="../templates", static_folder="../static")


@movie.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":  
        return render_template("select.html", movie_datas = select_movie())
    else:
        return render_template("add.html")


@movie.route("/added")
def added():
    save_movie()
    return redirect(url_for("home.index"))


@movie.route("/delete")
def delete_movie():
    movie_deleter(request.args.get("id"))
    return redirect(url_for("home.index"))
