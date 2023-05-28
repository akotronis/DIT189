import requests
from . import app
from .database import DataBase


def initialize_db():
    with app.app_context():
        db = DataBase()
        db.create_tables()
        db.initialize()

if __name__ == '__main__':
    initialize_db()