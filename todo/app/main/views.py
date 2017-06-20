from . import main
from ..models import Todo
from .forms import TodoForm
from .. import db
from flask import render_template, request, redirect, url_for, flash

@main.route('/', methods=["POST", "GET"])
def index():
    form = TodoForm()
    if form.validate_on_submit():
        body = form.body.data
        todo = Todo(body=body, done=False)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('.index'))

    todos = Todo.query.order_by(Todo.timestamp.desc()).all()
    return render_template('index.html', todos=todos, form=form)

@main.route('/done/<int:id>')
def done(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo is None:
        flash('Not found the todo.')
        return redirect('.index')
    #flash('Found the todo')
    todo.done = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('.index'))

@main.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('.index'))
