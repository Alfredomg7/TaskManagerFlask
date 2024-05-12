import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ltUN7a9JZcrzQWFmKtU_QA')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'P+bAN55/87EJ59Y3jS6r+Rnhy6lAxol1yo/hB0GeHfw=')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../instance/test.db')
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your-email@example.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your_password')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    PROPAGATE_EXCEPTIONS = False

class ProductionConfig(Config):
    DEBUG = False