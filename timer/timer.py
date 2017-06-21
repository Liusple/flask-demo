# coding: utf-8

from flask import Flask, render_template, redirect, url_for, flash, request
import  re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'

@app.route('/')
def index():
    return redirect(url_for('timer',num=25*60))

@app.route('/<int:num>s')
@app.route('/<int:num>')
def timer(num):
    return  render_template('index.html', num=num)

@app.route('/custom', methods=['POST', 'GET'])
def custom():
    time = request.form.get('time', 60)
    m = re.match('\d+[smh]?$', time)
    if m is None:
        flash('请输入一个有效时间，例如34, 20s, 10m, 1h')
        return redirect(url_for('index'))
    if time[-1] not in 'smh':
        return redirect(url_for('timer', num=int(time)))
    else:
        type = {'s':'timer', 'm':'minutes', 'h':'hours'}
        return redirect(url_for(type[time[-1]], num=int(time[:-1])))

@app.route('/<int:num>m')
def minutes(num):
    return redirect(url_for('timer', num=60*num))

@app.route('/<int:num>h')
def hours(num):
    return redirect(url_for('timer', num=3600*num))

@app.errorhandler(404)
def page_not_found(e):
    flash('访问地址出错，鼠标放在问号上了解更多')
    return redirect(url_for('timer', num=20))

if __name__ == '__main__':
    app.run(debug=True)
