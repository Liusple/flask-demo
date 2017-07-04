# coding=utf-8
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))