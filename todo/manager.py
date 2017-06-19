from app import create_app, db
from flask_script import Manager,Shell
import  os
from livereload import Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Todo

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


if '__main__' == __name__:
    manager.run()
