# coding=utf-8
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash        ###


class Permission:
    FOLLOW = 0x01  #没有逗号
    COMMENT = 0x02
    WRITE = 0x04
    MODERATE = 0x08
    ADMIN = 0x80

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")
    name = db.Column(db.String(64), unique=True)##unique
    default = db.Column(db.Boolean, default=False)

    @staticmethod
    def create_roles(): #not have self
        roles = {
            "User":(Permission.WRITE |
                    Permission.COMMENT |
                    Permission.FOLLOW, True),
            "Admin":(0xff, False),
            "Moderator":(Permission.WRITE |
                         Permission.COMMENT |
                         Permission.FOLLOW |
                         Permission.MODERATE, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r, permissions=roles[r][0], default=roles[r][1])
                db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    @property
    def password(self):
        raise AttributeError("Password can not be seen")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  #self.password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    timestamp = db.Column(db.DateTime, default=datetime.now)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))