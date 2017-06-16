# coding:utf-8

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard string to guess'
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login1', methods=['POST', 'GET'])
def login1():
    form = LoginForm()
    #if form.validate_on_submit():
    if request.method == 'POST' and form.validate():
        name = form.name.data
        age = form.age.data
        flash('提交的名字是:%s' %name, 'info')
        flash('提交的年龄是:%s' %age, 'info')
        return redirect(url_for('login2'))
    return render_template('login1.html', form=form)

@app.route('/login2', methods=['POST', 'GET'])
def login2():
    if request.method == 'POST':
        address = request.form.get('address')
        flash('提交的地址是:%s' %address, 'warning')
        return redirect(url_for('index'))
    return render_template('login2.html')

class LoginForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired(message='请输入姓名'), Length(2, 20, message='请输入2~20个字符')])
    age = IntegerField('年龄', validators=[DataRequired(message='请输入年龄')])
    submit = SubmitField('提交')

    def validate_age(self, field):
        if field.data > 30:
            raise ValidationError('年龄必须小于30岁')

if __name__ == '__main__':
    app.run(debug=True)
