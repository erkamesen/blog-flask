from flask import Blueprint, flash, redirect, url_for, render_template, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, CommentForm
from models import User, Comment, db, BlogPost
from flask_login import login_user, current_user, logout_user
import requests
from pkg.telegram import Logger

user = Blueprint("user", __name__, template_folder="../templates",
                 static_folder="../static")


@user.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@user.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)




@user.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if request.args.get("comment_text"):
        print("deneme")
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("user.login"))
        

        new_comment = Comment(
            text=request.args.get("comment_text"),
            comment_author=current_user,
            parent_post=requested_post
            )
        
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("admin.show_post", post_id = post_id))
    else:
        return render_template("post.html", post=requested_post, form=form)






@user.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
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

    return render_template("register.html", form=form, current_user=current_user)


@user.route('/login', methods=["GET", "POST"])
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
            return redirect(url_for('home.get_all_posts'))
    return render_template("login.html", form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.get_all_posts'))




