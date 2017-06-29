# coding: utf-8
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ForgetPasswordForm, ResetPasswordForm, ChangeEmailForm
from flask import render_template, redirect, url_for, request, flash
from .. import db
from ..models import User
from flask_login import login_user, current_user, login_required, logout_user
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


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(u"你已注销", "info")
    return redirect(url_for("main.index"))


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
        flash(user.email, "info")
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
    if current_user.is_authenticated:
        current_user.ping()
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
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


@auth.route("/change-password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        #验证旧密码是否正确放在这里处理
        if current_user.verify_password(form.password.data):
            current_user.password = form.password1.data
            db.session.add(current_user)
            db.session.commit()
            flash(u"密码修改成功", "success")
            return redirect(url_for("main.index"))
        else:
            flash(u"原密码无效", "danger")
    return render_template("auth/change_password.html", form=form)


@auth.route("/forget-password", methods=["POST", "GET"])
def forget_password():
    form = ForgetPasswordForm()
    if not current_user.is_anonymous:##
        return redirect(url_for("main.index"))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_reset_token()##
            send_email(form.email.data, u"忘记密码", "email/forget-password", token=token)
            flash(u"请登录邮箱，点击链接重置密码", "info")
        else:
            flash(u"输入的邮箱无效", "danger")
        return redirect(url_for("main.index"))
    return render_template("auth/forget_password.html", form=form)


@auth.route("/reset-password/<token>", methods=["POST", "GET"])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(u"email无效", "danger")
            return redirect(url_for("main.index"))
        elif user.verify_reset(token, form.password.data):#
            flash(u"密码已经重置了", "success")
            return redirect(url_for("auth.login"))
        else:
            flash(u"验证失败，请重新验证")
            return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/change-email", methods=["POST", "GET"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_token(new_email)
            send_email(new_email, u"修改邮箱", "email/change_email", user=current_user, token=token)
            flash(u"有一封邮件发到了新的邮箱，请验证", "info")
            return redirect(url_for("main.index"))
        else:
            flash(u"密码错误", "danger")
    #一直漏写form
    return render_template("auth/change_email.html", form=form)


@auth.route("/change-email/<token>")
@login_required
def change_email(token):
    if current_user.verify_email(token):
        flash(u"邮箱重置成功", "success")
    else:
        flash(u"邮箱重置失败", "danger")
    return redirect(url_for("main.index"))