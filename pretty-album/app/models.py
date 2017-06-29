# coding:utf-8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    CREATE_ALBUMS = 0x04
    MODERATE_COMMENTS = 0x08
    ADMIN = 0x80


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)##
        if self.role is None:
            if self.email == current_app.config["ALBUM_ADMIN"]:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)##
        db.session.commit()

    @property
    def password(self):
        raise AttributeError(u"无法获取密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id})

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if self.id != data.get("confirm"):
            return False
        self.confirmed = True
        ##care
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.id})

    def verify_reset(self, token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("reset") != self.id:
            return False
        #用self.password修改密码
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_email_token(self, email, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        #not s.dumps({}, {})
        return s.dumps({"change_email":self.id, "new_email":email})

    def verify_email(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("change_email") == self.id:
            #判断get有无
            new_email = data.get("new_email")
            if new_email is None:
                return False
            #self.query
            if self.query.filter_by(email=new_email).first():
                return False
            self.email = new_email
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def can(self, permissions):##
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMIN)  #

    def __repr__(self):
        return "<User %s>" % self.name


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")#not dynamic="lazy"

    @staticmethod
    def create_roles():
        roles = {
            "Admin":(0xff, False),
            "User":(Permission.COMMENT |
                    Permission.FOLLOW |
                    Permission.CREATE_ALBUMS, True),
            "Moderator":(Permission.COMMENT |
                         Permission.FOLLOW |
                         Permission.MODERATE_COMMENTS |
                         Permission.CREATE_ALBUMS, False)
        }
        for k in roles:
            role = Role.query.filter_by(name=k).first()
            if role is None:
                role = Role(name=k)
            role.permissions = roles[k][0]
            role.default = roles[k][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Role %s>" % self.name

#
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
