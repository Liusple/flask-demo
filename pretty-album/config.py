__author__ = 'lius'

import os

basedir = os.getcwd()

class BaseConfig:
    SECRET_KEY = "forever young"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "18158135171@163.com"
    MAIL_PASSWORD = "85271082s"
    MAIL_SENDER = "18158135171@163.com"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.sqlite")

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite")

config={
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}