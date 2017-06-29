# coding=utf-8

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, BooleanField, SubmitField

class EditProfileForm(FlaskForm):
    location = StringField(u"地区", validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我', render_kw={'rows': 8})#
    status = StringField(u"签名", validators=[Length(0, 64)])
    submit = SubmitField(u"提交")




