import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4142141rsaasfd;o3w485a;o8hnp'
    DB_PASS = os.environ.get('DB_PASS')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://orabbits:{}@localhost/orabbits".format(Config.DB_PASS)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://orabbits:{}@localhost/orabbits_test".format(Config.DB_PASS)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
