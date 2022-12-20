from flask import Blueprint, flash, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
from models import User, Movie, db
from flask_login import login_user, current_user, logout_user
from packages import login_manager
from controller import email_check
import requests
from controller import MOVIEURL, MOVIEAPI


bp = Blueprint("user", __name__, template_folder="../templates",
               static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if email_check(email=form.email.data):
            if User.query.filter_by(email=form.email.data).first():
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for("user.login"))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home.get_all_posts"))
        else:
            return 

    return render_template("register.html", form=form, current_user=current_user)


@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('user.login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('user.login'))
        else:
            login_user(user)
            return redirect(url_for('home.get_all_posts', current_user=current_user))
    return render_template("login.html", form=form, current_user=current_user)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.get_all_posts'))



## MOVIE PART ##


@bp.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        params = {
    "api_key":MOVIEAPI,
    "query":request.form.get("title")
    }
        response = requests.get(MOVIEURL, params=params)
        titlelist = [datas["original_title"] for datas in response.json()["results"]]
        datelist = [datas["release_date"] for datas in response.json()["results"]]
        idlist = [datas["id"] for datas in response.json()["results"]]
        datas =zip(idlist,titlelist,datelist)
        return render_template("select.html", datas = datas)
    else:
        return render_template("add.html")
    
    

@bp.route("/added", methods=["GET","POST"])
def added():
    movie_id = request.args.get("id")
    query = request.args.get("title")
    params = {
    "api_key":MOVIEAPI,
    "query":query
    }
    response = requests.get(MOVIEURL, params=params)
    for movieinfo in response.json()["results"]:
        if int(movieinfo["id"]) == int(movie_id):
                new_movie = Movie(
            title= movieinfo["original_title"],
            year= movieinfo["release_date"].split("-")[0],
            description= movieinfo["overview"],
            rating= float(movieinfo["vote_average"]),
            ranking= 5,
            review= "",
            img_url=f"https://image.tmdb.org/t/p/w500{movieinfo['poster_path']}")
                
                db.session.add(new_movie)
                db.session.commit()
                return redirect(url_for("home.get_all_posts"))
            
            
@bp.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home.get_all_posts"))
                

