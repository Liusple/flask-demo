# coding=utf-8
import os

basedir = os.getcwd()

class BaseConfig():
    SECRET_KEY = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.sqlite")##


config={
    "dev": DevelopmentConfig,
    "default": DevelopmentConfig
}
