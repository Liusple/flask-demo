# coding=utf-8

from flask import Blueprints

api = Blueprints("api", __name__)

from . import authentication, users, posts, comments, errors
