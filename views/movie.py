from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Movie
from controller import MOVIEAPI, MOVIEURL
import requests
movie = Blueprint("movie", __name__, template_folder="../templates", static_folder="../static")



@movie.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        params = {
            "api_key": MOVIEAPI,
            "query": request.form.get("title")
        }
        response = requests.get(MOVIEURL, params=params)
        try:
            title_list = [datas["original_title"]
                        for datas in response.json()["results"]]
            date_list = [datas["release_date"]
                        for datas in response.json()["results"]]
            id_list = [datas["id"] for datas in response.json()["results"]]
            poster_list = [datas["poster_path"] for datas in response.json()["results"]]
            datas = zip(id_list, title_list, date_list, poster_list)
            return render_template("select.html", datas=datas)
        except:
            return render_template("add.html")
    else:
        return render_template("add.html")


@movie.route("/added")
def added():
    movie_id = request.args.get("id")
    query = request.args.get("title")
    params = {
        "api_key": MOVIEAPI,
        "query": query
    }
    response = requests.get(MOVIEURL, params=params)
    for movieinfo in response.json()["results"]:
        if int(movieinfo["id"]) == int(movie_id):
            new_movie = Movie(
                title=movieinfo["original_title"],
                year=movieinfo["release_date"].split("-")[0],
                description=movieinfo["overview"],
                rating=float(movieinfo["vote_average"]),
                ranking=5,
                review="",
                img_url=f"https://image.tmdb.org/t/p/w500{movieinfo['poster_path']}")

            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for("home.get_all_posts"))


@movie.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home.get_all_posts"))
