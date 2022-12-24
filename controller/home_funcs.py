from models import BlogPost, Movie

def get_posts_and_movies():
    """
        Return 
    posts  - List
    movies - List
    """
    posts = BlogPost()
    movies = Movie() 
    
    return posts.get_all_posts(), movies.get_all_movies()
    