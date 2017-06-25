# coding: utf-8
from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

