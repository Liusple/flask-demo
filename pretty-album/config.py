__author__ = 'lius'

import os

basedir = os.getcwd()

class BaseConfig:
    SECRET_KEY = "forever young"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
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