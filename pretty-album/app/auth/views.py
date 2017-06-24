# coding: utf-8
from . import auth
from .forms import LoginForm, RegisterForm
from flask import render_template, redirect, url_for, request, flash
from .. import db
from ..models import User


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            flash(u"登录成功")
            return render_template("index.html")
        else:
            flash(u"用户名或者密码错误，请重新登录", "danger")
    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(u"注册成功，可以登录了", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)