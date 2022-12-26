import requests
from dotenv import load_dotenv
from models import Movie
import os
from flask import request, render_template
from pkg.telegram import Logger

load_dotenv()

logger = Logger(token=os.getenv("telegramApi"), chat_id=os.getenv("chatID"))


def get_movies(query):
    """
    This is the request function. If the status code is greater than 400,
    the logger sends us a warning message.
    """
    params = {
        "api_key": os.getenv('MOVIEAPI'),
        "query": query
    }
    response = requests.get(os.getenv("MOVIEURL"), params=params)
    if response.status_code > 400:
        message = "I detected a problem for the TMDB API please check as soon as possible"
        logger.warning(message=message)
        return render_template("index.html")
    else:
        result = response.json()["results"]
        return result


def add_movie(title, year, description, rating, img_url):
    """
    Add movie to database.
    """
    movie = Movie()
    movie.title = title
    movie.year = year
    movie.description = description
    movie.rating = rating
    movie.img_url = img_url
    movie.add_movie_to_database()
 
  
def save_movie():
    """
    With the get_movies() function, we compare the movies we fetch from our API with the
    id we get as args. then we add it to the database with add_movie()
    """
    movie_id = request.args.get("id")
    query = request.args.get("title")
    
    for movie_info in get_movies(query=query):
        if int(movie_info["id"]) == int(movie_id):
            add_movie(
                title=movie_info.get("original_title"),
                year=movie_info.get("release_date"),
                description=movie_info.get("overview"),
                rating=float(movie_info.get("vote_average")),
                img_url=f"https://image.tmdb.org/t/p/w500{movie_info.get('poster_path')}")
   
   
def movie_deleter(id):
    """
    Delete the requested movie with id
    """
    requested_movie = Movie()
    requested_movie.del_movie(id=id)


def select_movie():
    title = request.form.get("title")
    result = get_movies(query=title)

    movie_list = [[movie.get("id"), movie.get("original_title"), movie.get("release_date"),
                movie.get("poster_path")] for movie in result]
    return movie_list
