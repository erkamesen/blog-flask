from flask import Blueprint, flash, redirect, url_for, render_template, request
from werkzeug.security import check_password_hash
from forms import RegisterForm, LoginForm, CommentForm, ContactForm
from models import User, BlogPost
from flask_login import login_user, current_user, logout_user
from controller.user_funcs import contact_me, new_comment, new_user


user = Blueprint("user", __name__, template_folder="../templates",
                 static_folder="../static")


@user.route("/about")
def about():
    return render_template("about.html")


@user.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_me()
        return redirect(url_for("home.index"))
    else:
        return render_template("contact.html", form=form)



@user.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if request.args.get("comment_text"):
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("user.login"))    

        new_comment(request.args.get("comment_text"),
                    current_user,
                    requested_post)
        
        return redirect(url_for("user.show_post", post_id = post_id))
    else:
        return render_template("post.html", post=requested_post, form=form)


@user.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("user.login"))

        new_user(password = form.email.data,
                 email = form.email.data,
                 name = form.name.data)
        login_user(new_user)
        return redirect(url_for("home.index"))

    return render_template("register.html", form=form, current_user=current_user)


@user.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('user.login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('user.login'))
        else:
            login_user(user)
            return redirect(url_for('home.index'))
    return render_template("login.html", form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))




