# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="Needed")])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="Needed")])
    submit = SubmitField("Submit")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Old Password", validators=[DataRequired(message="Needed")])
    password1 = PasswordField("New Password", validators=[DataRequired(message="Needed")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(message="Needed"), EqualTo("password1")])##
    submit = SubmitField("Submit")

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError("Invalid Password")

