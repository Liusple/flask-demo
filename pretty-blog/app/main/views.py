# coding=utf-8

from . import main
from .forms import EditProfileForm, PostForm
from flask import redirect, url_for,render_template, flash, abort
from flask_login import current_user, login_required
from .. import db
from ..models import User, Post

@main.route("/", methods=["POST", "GET"])
def index():
    form = PostForm()
    #permission
    if form.validate_on_submit():
        post = Post(author=current_user._get_current_object(), body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash("Post cuccess")
        return redirect(url_for("main.index"))
    return render_template("index.html", form=form)


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