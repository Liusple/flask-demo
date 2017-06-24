__author__ = 'lius'

class BaseConfig:
    SECRET_KEY = "forever young"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


config={
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}