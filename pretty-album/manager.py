# coding:utf-8

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role

app = create_app("default")

manager = Manager(app)
migrate = Migrate(app, db)


def make_context_shell():
    return dict(db=db, app=app, User=User, Role=Role)


manager.add_command("db", MigrateCommand)
manager.add_command("shell", Shell(make_context=make_context_shell))


if __name__ == "__main__":
    manager.run()
