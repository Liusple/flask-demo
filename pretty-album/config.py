__author__ = 'lius'

import os

basedir = os.getcwd()

class BaseConfig:
    SECRET_KEY = "forever young"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SENDER = os.environ.get("MAIL_SENDER")
    ALBUM_ADMIN = "18158135171@qq.com"
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/app/static/img/'

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