import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_AUTO_RELOAD = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
