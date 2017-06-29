# coding:utf-8

from flask import render_template, flash, redirect, request, abort, url_for
from . import main
from flask_login import login_required
from .forms import EditProfileForm
from ..models import User, Role
from flask_login import current_user
from .. import db

@main.route("/")
def index():
    flash(request.endpoint, "info")
    return render_template("index.html")

@main.route("/secret")
@login_required
def secret():
    return render_template("test.html")


@main.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(403)
    return render_template("user.html", user=user)


@main.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.status = form.status.data
        db.session.add(current_user)
        db.session.commit()
        flash(u"资料更新成功", "success")
        return redirect(url_for("main.user", username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.status.data = current_user.status
    return render_template("edit_profile.html", form=form)
