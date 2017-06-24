# coding: utf-8

from . import auth
from .forms import LoginForm
from flask import render_template, redirect, url_for, request, flash


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    username = "alex"
    if form.validate_on_submit():
        username = form.username.data
    return render_template("auth/login.html", form=form, username=username)

