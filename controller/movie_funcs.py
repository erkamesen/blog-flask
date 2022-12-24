import requests
from dotenv import load_dotenv
from models import Movie
import os
from flask import request

load_dotenv()


def get_movies_from_tmdb(query):
    params = {
        "api_key": os.getenv('MOVIEAPI'),
        "query": query
    }
    response = requests.get(os.getenv("MOVIEURL"), params=params)
    response.raise_for_status()
    result = response.json()["results"]
    
    return result


def will_be_added_movie(title, year, description, rating, img_url):
    movie = Movie()
    movie.title = title
    movie.year = year
    movie.description = description
    movie.rating = rating
    movie.img_url = img_url
    movie.add_movie_to_database()
 
    
    
  
def movie_adder():
    movie_id = request.args.get("id")
    query = request.args.get("title")
    for movie_info in get_movies_from_tmdb(query=query):
        if int(movie_info["id"]) == int(movie_id):
            will_be_added_movie(
                title=movie_info["original_title"],
                year=movie_info["release_date"].split("-")[0],
                description=movie_info["overview"],
                rating=float(movie_info["vote_average"]),
                img_url=f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}")
   


def movie_deleter(id):
    will_be_deleted = Movie()
    will_be_deleted.del_movie(id=id)
    
    
def movie_lister():
    title = request.form.get("title")
    result = get_movies_from_tmdb(query=title)
    
    title_list = [datas["original_title"]
                      for datas in result]
    try:
        date_list = [datas["release_date"].split("-")[0]
                    for datas in result]
    except KeyError:
        date_list = ["-" for i in range(len(title_list))]
            
    id_list = [datas["id"] for datas in result]
    poster_list = [datas["poster_path"]
                       for datas in result]
    datas = zip(id_list, title_list, date_list, poster_list)   
    return datas