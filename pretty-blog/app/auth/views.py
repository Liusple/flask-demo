# coding=utf-8
from flask_login import login_required, login_user, logout_user, current_user
from flask import url_for, render_template, flash, request, redirect
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from ..models import User
from .. import db

@auth.before_app_request##
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            #remember
            login_user(user)
            flash("Login success")
            return redirect(request.args.get("next") or url_for("main.index"))###
        else:
            flash("Login failed")
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Logout success")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("Register success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/change-password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password1.data
        db.session.add(current_user)
        db.session.commit()
        flash("Password change success")
        return redirect(url_for("main.index"))
    return render_template("auth/change_password.html", form=form)