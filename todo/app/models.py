from . import db


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(64), unique=True)
    done = db.Column(db.Boolean)
    def __repr__(self):
        return '<Todo %r> %self.name'
