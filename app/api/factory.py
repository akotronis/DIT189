import os

from dotenv import load_dotenv
from flask import Flask
from flask_oidc_ext import OpenIDConnect

from .config.config import config_by_name
from .db import db


from .keycloak import KeycloakAPI

# Necessary for creating tables
from .models import *


# Connect OpenIDConnect to the app
oidc = OpenIDConnect()


# Function creating app object
def create_app(config_name):
    app = Flask(__name__)

    # Load configurations from config module
    app.config.from_object(config_by_name[config_name])

    # Load environment variables from .env (.flaskenv)
    load_dotenv()

    # Initialize Flask-SQLAlchemy and pass app object to connect with
    db.init_app(app)

    # Initialize OpenIDConnect and pass app object to connect with
    oidc.init_app(app)

    return app