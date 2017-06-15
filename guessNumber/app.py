# coding:utf-8

import random
from flask import Flask, render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    session['number'] = random.randint(0, 1000)
    session['times'] = 4
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']
    result = session.get('number')
    form = GuessForm()
    if form.validate_on_submit():
        answer = form.number.data
        times -= 1
        session['times'] = times
        if answer > result and times > 0:
            flash('大了 还有%s次机会' % times, 'warning')
        elif answer < result and times > 0:
            flash('小了 还有%s次机会' % times, 'warning')
        elif answer == result:
            flash('猜对了 数字是%s' % answer, 'success')
            return redirect(url_for('index'))
        if times == 0:
            flash('游戏结束 数字是%s' % result, 'danger')
            return redirect(url_for('index'))
        return redirect(url_for('guess'))
    return render_template('guess.html', form=form)


class GuessForm(FlaskForm):
    number = IntegerField('输入一个整数（0~1000）', validators=[DataRequired('请输入一个数字'),
                                                        NumberRange(0, 1000, '请输入0~1000以内的数字')])
    submit = SubmitField('提交')


if __name__ == '__main__':
    app.run(debug=True)
