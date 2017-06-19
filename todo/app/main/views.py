from . import main
from ..models import Todo
from .forms import TodoForm
from .. import db
from flask import render_template, request, redirect, url_for


@main.route('/')
def index():
    form = TodoForm()
    todos = Todo.query.all()

    return render_template('index.html', todos=todos, form=form)


@main.route('/add-todo', methods=["POST", "GET"])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        body = form.body.data
        todo = Todo(body=body, done=False)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('.index'))