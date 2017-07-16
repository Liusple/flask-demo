# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Regexp
from flask_login import current_user
from ..models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="Needed")])
    #remember me
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    #regexp
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password1 = PasswordField("Password", validators=[DataRequired(message="Needed")])
    password2 = PasswordField("Confirm passowrd", validators=[DataRequired(message="Needed"), EqualTo("password1", message="Passwords must match")])
    submit = SubmitField("Submit")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():##not field.username
            raise ValidationError("Invalid username")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Old Password", validators=[DataRequired(message="Needed")])
    password1 = PasswordField("New Password", validators=[DataRequired(message="Needed")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(message="Needed"), EqualTo("password1", message="Password must match")])##
    submit = SubmitField("Submit")

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError("Invalid Password")

