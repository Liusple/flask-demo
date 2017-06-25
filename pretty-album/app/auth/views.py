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
    flash(request.endpoint, "info")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            flash(u"登录成功", "info")
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash(u"用户名或者密码错误，请重新登录", "danger")
    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    flash(request.endpoint, "info")
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    confirmed=False)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirm_token()
        send_email(user.email, u"新用户请认证", "email/confirm", user=user, token=token)
        flash(u"邮箱，请认证", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash(request.endpoint, "info")
        flash(u"认证成功", "info")
    else:
        flash(u"认证时间已过，认证失败，请重新认证", "info")
    return redirect(url_for("main.index"))


@auth.before_app_request
def before_request():
    print(request.endpoint)
    print(current_user.is_authenticated)
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != "auth."\
            and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
#not login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirm_token()
    send_email(current_user.email, u"认证", "email/confirm", user=current_user, token=token)
    flash(u"邮件已发送，请点击认证", "info")
    return redirect(url_for("main.index"))



