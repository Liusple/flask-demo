from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    body = StringField('Something to do', validators=[DataRequired(message="Input something")])
    submit = StringField('Add')