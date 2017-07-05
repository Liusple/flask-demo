# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class EditProfileForm(FlaskForm):
    location = StringField("Location", validators=[Length(1, 64)])
    about_me = TextAreaField("About_me")
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    body = TextAreaField("Post", validators=[DataRequired(message="Need Post")])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(message="Need Comment")])
    submit = SubmitField("Submit")