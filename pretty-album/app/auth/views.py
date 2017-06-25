# coding: utf-8
from . import auth
from .forms import LoginForm, RegisterForm
from flask import render_template, redirect, url_for, request, flash
from .. import db
from ..models import User
from flask_login import login_user, current_user, login_required
from ..email import send_email


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            flash(u"登录成功")
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash(u"用户名或者密码错误，请重新登录", "danger")
    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirm()
        send_email(user.email, u"新用户请认证", "email/confirm", user=user, token=token)
        flash(u"邮箱，请认证", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirm(token):
        print("asdf success")
    else:
        print("asdf failed")
    return render_template("test.html")








