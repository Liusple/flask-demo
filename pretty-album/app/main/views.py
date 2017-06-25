# coding:utf-8

from flask import render_template, flash, redirect, request
from . import main
from flask_login import login_required


@main.route("/")
def index():
    flash(request.endpoint, "info")
    return render_template("index.html")

@main.route("/secret")
@login_required
def secret():
    return render_template("index.html")
