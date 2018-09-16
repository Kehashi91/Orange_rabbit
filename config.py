"""Configuration file for class-based flask configuration."""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # base

    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4142141rsaasfd;o3w485a;o8hnp'
    DB_PASS = os.environ.get('DB_PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

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

class ProductionConfig(Config):
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = "postgresql://orabbits:{}@localhost/orabbits_prod".format(Config.DB_PASS)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig
}
