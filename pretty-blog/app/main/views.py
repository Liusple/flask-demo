# coding=utf-8

from . import main
from .forms import EditProfileForm, PostForm, CommentForm
from flask import redirect, url_for,render_template, flash, abort, request
from flask_login import current_user, login_required
from .. import db
from ..models import User, Post, Comment

@main.route("/", methods=["POST", "GET"])
def index():
    form = PostForm()
    #permission
    if form.validate_on_submit():
        post = Post(author=current_user._get_current_object(), body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash("Post success")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template("index.html", form=form, posts=posts, pagination=pagination)


@main.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data  #if empty
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash("Edit profile success")
        return redirect(url_for("main.user", username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)


@main.route("/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)


@main.route("/post/<int:id>", methods=["POST", "GET"])
def post(id):
    post = Post.query.get_or_404(id)    #
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, author=current_user._get_current_object(), post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Comment success")
        return redirect(url_for("main.post", id=post.id))##post.id
    page = request.args.get("page", 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=20, error_out=False)              ##
    comments = pagination.items
    return render_template("post.html", posts=[post], comments=comments, pagination=pagination, form=form)

@main.route("/edit-post/<int:id>", methods=["POST", "GET"])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash("Edit success")
        return redirect(url_for("main.post", id=post.id))
    form.body.data = post.body
    return render_template("edit_post.html", form=form)






