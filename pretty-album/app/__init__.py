# coding: utf-8
__author__ = 'lius'


from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#bootstrap = Bootstrap()
#db = SQLAlchemy()
app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #bootstrap.init_app(app)
    #db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")


    return app

