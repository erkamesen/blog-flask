from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import request

db = SQLAlchemy()




##CONFIGURE TABLE
class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    
    def __repr__(self) -> str:
        return f"name: {self.name}"
    
    def get_dict(self):
        return {column.name:getattr(self.column.name) for column in self.__table__Columns}
    
    def __str__(self) -> str:
        return f"User's name: {self.name}, User's Posts: {self.posts}, User's Comments: {self.comments}"
    
    
    def get_all_users(self):
        user_list = self.query.get.all()
        return user_list
    
        
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")

    
    def __str__(self) -> str:
        return f"Post's Title: {self.title}, Post's Subtitle: {self.subtitle}, Post's Create Date: {self.date}, \
                Post's Content: {self.body}, Post's Image URL: {self.img_url}"
         
    @classmethod
    def delete_post(cls, post_id):
        post_to_delete = cls.query.get(post_id)
        db.session.delete(post_to_delete)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text, nullable=False)

    def __str__(self) -> str:
        return f"Comment'Author: {self.comment_author}, Comment's Content: {self.text}"
     

### TMDB ###  
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    ranking = db.Column(db.Integer, nullable = False)
    review = db.Column(db.String(400), nullable = False)
    img_url = db.Column(db.String, nullable = False)
    
    @classmethod
    def get_all_movies(cls):
        """index html ye get methodunda yollanacak

        Returns:
            list: --
        """
        movies = cls.query.order_by(cls.rating).all()
        
        for i in range(len(movies)):
            movies[i].ranking = len(movies) - i
        db.session.commit()
        
        return movies
        
    
    def delete_movie(self, id):
        """Filmi silmek için kullan. template içine:
        <a href="{{ url_for('delete_movie', id=movie.id)  }}" class="button delete-button">Delete</a>
        ile args yolla ve fonksiyonda yakalayıp sil.

        Args:
            integer: _description_
        """
        movie_id = request.args.get("id")
        movie = Movie.query.get(movie_id)
        db.session.delete(movie)
        db.session.commit()
        

    
    