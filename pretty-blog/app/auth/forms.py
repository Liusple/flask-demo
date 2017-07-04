# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="Needed")])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Needed"), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="Needed")])
    submit = SubmitField("Submit")

