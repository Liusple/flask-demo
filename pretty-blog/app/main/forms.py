# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ..models import User, Role

class EditProfileForm(FlaskForm):
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")


class EditProfileAdminForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username"), Length(1, 64)])
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About me")
    role = SelectField("Role", coerce=int)###
    submit = SubmitField("Submit")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        #not Role.query().order_by
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        ###
        if self.user.username != field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError("Username in use")


class PostForm(FlaskForm):
    body = TextAreaField("Post", validators=[DataRequired(message="Need Post")])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    body = TextAreaField("Enter your comment", validators=[DataRequired(message="Need Comment")])
    submit = SubmitField("Submit")