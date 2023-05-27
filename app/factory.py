import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from config.config import config_by_name
from db import db

# Necessary for creating tables
import models


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

    # Not needed with Flask-Migrate
    with app.app_context():
        # Create tables IF NOT EXIST
        db.create_all() 

    return app