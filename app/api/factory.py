import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from .blueprints import register_blueprints
from .config.config import config_by_name
from .db import db


# Necessary for creating tables
from .models import *


# Function creating app object
def create_app(config_name):
    app = Flask(__name__)

    # Load configurations from config module
    app.config.from_object(config_by_name[config_name])

    # Load environment variables from .env (.flaskenv)
    load_dotenv()

    # Initialize Flask-SQLAlchemy and pass app object to connect with
    db.init_app(app)

    # Connect flask_smorest to the app
    api = Api(app)

    # Register Blueprints
    register_blueprints(api)

    return app