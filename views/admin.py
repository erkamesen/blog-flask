from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user
from forms import CommentForm, CreatePostForm
from models import db, BlogPost, Comment
from controller import admin_only
from datetime import date


admin = Blueprint("admin", __name__, template_folder="../templates", static_folder="../static")




@admin.route("/post/<int:post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("show_post", post_id = post_id))
    else:
        return render_template("post.html", post=requested_post, form=form)




@admin.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home.get_all_posts"))

    return render_template("make-post.html", form=form, current_user=current_user)


@admin.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)



@admin.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home.get_all_posts'))
