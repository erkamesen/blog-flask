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
    
    def get_by(cls, object):
        cls.query.filter_by(object).first()
        
    def add_user(self):
        db.session.add(self)
        db.session.commit() 
    
        
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
    
    def get_all_posts(cls):
        posts = cls.query.all()
        print(posts)
        return posts
    
    @classmethod
    def get_post(cls, id):
        requested_post = cls.query.get(id)
        return requested_post
    
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
    
    def add_comment(self):
        db.session.add(self)
        db.session.commit()
     

### TMDB ###  
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), default="-")
    year = db.Column(db.Integer, default="-")
    description = db.Column(db.String, default="-")
    rating = db.Column(db.Float, default="-")
    img_url = db.Column(db.String, default="-")
    
    @classmethod
    def get_all_movies(cls):
        movies = cls.query.all() 
        print(movies)  
        return movies
       
       
       
    def add_movie_to_database(self):
        
        db.session.add(self)
        db.session.commit() 
    
    @classmethod
    def del_movie(cls, id):
        movie = cls.query.get(id)
        db.session.delete(movie)
        db.session.commit()
        

    
    