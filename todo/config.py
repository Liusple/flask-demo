import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    SECRET_KEY = 'hard to guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}