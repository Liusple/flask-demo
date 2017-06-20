from app import create_app, db
from flask_script import Manager,Shell
import  os
from livereload import Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Todo
from datetime import datetime

app = create_app(os.getenv('TODO_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Todo=Todo)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

@manager.command
def deal_time():
    todos = Todo.query.all()
    for todo in todos:
        todo.timestamp = datetime.utcnow()
        db.session.add(todo)
        db.session.commit()

@app.template_filter('format_time')
def format_time(time):
    return "%d.%d.%d %d:%d:%d" %(time.year, time.month, time.day, time.hour, time.minute, time.second)

if '__main__' == __name__:
    manager.run()
