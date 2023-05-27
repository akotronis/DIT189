import os
import secrets


basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = 'BookAPI'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
    SQLALCHEMY_ECHO = False


config_by_name = dict(
    prod=ProductionConfig,
    dev=DevelopmentConfig,
)