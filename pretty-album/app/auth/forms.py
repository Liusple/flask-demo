# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(message=u"请输入用户名")])
    password = PasswordField(u"密码", validators=[DataRequired(message=u"请输入密码")])
    remember = BooleanField(u"记住我")
    submit = SubmitField(u"登录")


class RegisterForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(message=u"请输入用户名"), Length(1, 64)])
    email = StringField(u"邮箱", validators=[Email(), DataRequired(message=u"请输入邮箱"), Length(1, 64)])
    password = PasswordField(u"密码", validators=[DataRequired(message=u"请输入密码")])
    password2 = PasswordField(u"确认密码", validators=[DataRequired(message=u"请输入密码"),
                                                 EqualTo("password", message=u"两次密码不一致")])
    submit = SubmitField(u"注册")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u"用户名已经被注册")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u"邮箱已经被注册")
