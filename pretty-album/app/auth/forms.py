# coding: utf-8

__author__ = 'lius'
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(message=u"请输入你的名字")])
    submit = SubmitField(u"登录")
