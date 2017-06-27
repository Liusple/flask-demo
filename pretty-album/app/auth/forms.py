# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError
from ..models import User
from flask_login import current_user #

class LoginForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(message=u"请输入用户名")])
    password = PasswordField(u"密码", validators=[DataRequired(message=u"请输入密码")])
    remember = BooleanField(u"记住我")
    submit = SubmitField(u"登录")


class RegisterForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(message=u"请输入用户名"), Length(1, 64)])
    email = StringField(u"邮箱", validators=[Email(u"邮箱格式不正确"), DataRequired(message=u"请输入邮箱"), Length(1, 64)])
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


class ChangePasswordForm(FlaskForm):
    password = PasswordField(u"旧密码", validators=[DataRequired(message="输入旧密码")])
    password1 = PasswordField(u"新密码", validators=[DataRequired(message=u"输入新密码")])
    password2 = PasswordField(u"确认新密码", validators=[DataRequired(message=u"确认新密码"),
                                                    EqualTo("password1", message=u"两次密码输的不一致")])
    submit = SubmitField(u"提交")


class ForgetPasswordForm(FlaskForm):
    email = StringField(u"邮箱", validators=[DataRequired(message=u"请输入邮箱"), Email(u"邮箱格式不正确")])
    submit = SubmitField(u"提交")


class ResetPasswordForm(FlaskForm):
    email = StringField(u"邮箱", validators=[DataRequired(message=u"请输入邮箱"), Email(u"邮箱格式不正确")])
    password = PasswordField(u"新密码", validators=[DataRequired(message=u"输入新密码")])
    password1 = PasswordField(u"确认新密码", validators=[DataRequired(message=u"确认新密码"),
                                                    EqualTo("password", message=u"两次密码输的不一致")])
    submit = SubmitField(u"提交")

class ChangeEmailForm(FlaskForm):
    email = StringField(u"新的邮箱", validators=[DataRequired(u"请输入邮箱"), Email(u"邮箱格式不正确")])
    password = PasswordField(u"密码", validators=[DataRequired(u"请输入密码")])
    submit = SubmitField(u"提交")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u"邮箱已经被注册")