# coding:utf-8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u"无法获取密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id})

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        data = s.loads(token)
        if (self.id != data.get("confirm")):
            return False
        else:
            return True


    def __repr__(self):
        return "<User %s>" % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
