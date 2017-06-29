# coding=utf-8
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from ..models import User, Role
from .. import db


class EditProfileForm(FlaskForm):
    location = StringField(u"位置", validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我', render_kw={'rows': 8})#
    status = StringField(u"签名", validators=[Length(0, 64)])
    submit = SubmitField(u"提交")

class EditProfileAdminForm(FlaskForm):
    email = StringField(u"邮箱", validators=[DataRequired(message=u"请输入邮箱"), Email()])##Email()
    confirmed = BooleanField(u"验证")
    location = StringField(u"位置")
    about_me = TextAreaField(u"关于我")
    status = StringField(u"签名")
    role = SelectField(u"角色", coerce=int)
    submit = SubmitField(u"提交")

    def __init__(self, user, *args, **kw):
        super(EditProfileAdminForm, self).__init__(*args, **kw)##__init__
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]##
        self.user = user

    def validate_email(self, field):
        if self.user.email != field.data and User.query.filter_by(email=field.data).first():##
            raise ValidationError(u"邮箱已经被注册")


