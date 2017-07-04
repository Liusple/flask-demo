# coding=utf-8
from flask_login import login_required, login_user, logout_user
from . import auth

@auth.route("/login", methods=["POST", "GET"])
def login():
    pass


@auth.route("/register", methods=["POST", "GET"])
def register():
    pass