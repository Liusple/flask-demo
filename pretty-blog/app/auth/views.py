# coding=utf-8
from flask_login import login_required, login_user, logout_user, current_user
from flask import url_for, render_template, flash, request, redirect
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User
from .. import db

@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
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
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Register success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


