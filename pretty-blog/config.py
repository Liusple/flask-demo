# coding=utf-8
import os

basedir = os.getcwd()

class BaseConfig():
    SECRET_KEY = "forever young"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.sqlite")##

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite")

config={
    "dev": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
