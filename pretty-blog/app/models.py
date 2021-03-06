# coding=utf-8
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash        ###
from flask import request, current_app, url_for
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.exceptions import ValidationError

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
                #role = Role(name=r, permissions=roles[r][0], default=roles[r][1])
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Follow(db.Model):
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    email = db.Column(db.String(64))
    image_hash = db.Column(db.String(64))
    about_me = db.Column(db.Text())##db.Text()
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    bugs = db.relationship("Bug", backref="author", lazy="dynamic")
    followed = db.relationship("Follow", foreign_keys=[Follow.follower_id],
                                backref=db.backref("follower", lazy="joined"),
                                lazy="dynamic",
                                cascade="all, delete-orphan")
    followers = db.relationship("Follow", foreign_keys=[Follow.followed_id],
                                backref=db.backref("followed", lazy="joined"),
                                lazy="dynamic",
                                cascade="all, delete-orphan")

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None
        #not self.followed.query.filter_by...

    def followed_by(self, user):
        #self.follower.filter_by(followed_id)
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        ###
        f = self.followed.filter_by(followed_id=user.id).first()###########
        if f:
            db.session.delete(f)
            db.session.commit()

    #care
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == "meixi":
                self.role = Role.query.filter_by(name="Admin").first()##
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.image_hash is None:###
            self.image_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

    @property
    def password(self):
        raise AttributeError("Password can not be seen")##

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  #self.password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def image(self, size=100, default="identicon", rating="g"):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.image_hash or hashlib.md5(self.email.encode("utf-8")).hexdigest()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(url=url, hash=hash, size=size, default=default, rating=rating)###

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)##
        db.session.commit()

    @staticmethod
    def add_self_follow():
        users = User.query.all()
        for u in users:
            if not u.is_following(u):
                u.follow(u)
                db.session.add(u)
        db.session.commit()


    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(username=forgery_py.internet.user_name(True),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     password=forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()      ##

    @staticmethod
    def generate_fake_data():
        from random import seed
        import forgery_py
        seed()
        users = User.query.all()
        for u in users:
            u.member_since = forgery_py.date.date(True)
            u.last_seen = datetime.utcnow()
            db.session.add(u)
        db.session.commit()

    ####
    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id==Post.author_id).filter(Follow.follower_id==self.id)
        #return db.session.query(Post).select_from(Follow).filter_by(follower_id=self.id).join(Post, Follow.followed_id == Post.author_id)

    @staticmethod
    def create_email_and_image_hash():
        import forgery_py
        from random import seed
        seed()
        users = User.query.all()
        for u in users:
            #if u.email is None:
            u.email = forgery_py.internet.email_address()
            #if u.image_hash is None:
            u.image_hash = hashlib.md5(u.email.encode("utf-8")).hexdigest()
            db.session.add(u)
        db.session.commit()

    def generate_auth_token(self, expiration):
        s = Serializer("SECRET",  expires_in=expiration)
        ss = s.dumps({"id": self.id})
        return s.dumps({"id": self.id}).decode("utf-8")##

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["id"])

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts', id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()##
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    def to_json(self):
        json_post = {
            "url": url_for("api.get_post", id=self.id, _external=True),
            "body": self.body,
            "timestamp": self.timestamp,
            "author": url_for("api.get_user", id=self.author_id, _external=True),
            "comments": url_for("api.get_post_comments", id=self.id, _external=True),
            "comment_count": self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get("body")
        if body is None or body == "":
            raise ValidationError("post does not have a body")
        return Post(body=body)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,  _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


class Bug(db.Model):
    __tablename__ = "bugs"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))