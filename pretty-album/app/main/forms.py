# coding=utf-8
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..models import User, Role
from .. import db
from .. import photos

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

class NewAlbumForm(FlaskForm):
    title = StringField(u"标题")
    about = TextAreaField(u"介绍")
    photo = FileField(u"图片", validators=[FileAllowed(photos, u"只能上传图片"), FileRequired(u"你还没有选择图片")])
    asc_order = SelectField(u"显示顺序", choices=[("True",u"按上传时间正序排列"), ("False",u"按上传时间倒序排列")])
    no_public = BooleanField(u"私密相册")
    no_comment = BooleanField(u"禁止评论")
    submit = SubmitField(u"提交")


class CommentForm(FlaskForm):
    body = TextAreaField(u"评论")
    submit = SubmitField(u"提交")

