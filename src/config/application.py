import os

from logging.config import dictConfig
from src.config.logger import CONFIG


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_SORT_KEYS = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    dictConfig(CONFIG)


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
    }
