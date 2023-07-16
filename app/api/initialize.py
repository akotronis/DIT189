import requests
from . import app
from .database import DataBase as DB


def initialize_db():
    with app.app_context():
        DB.create_tables()
        DB.initialize()

if __name__ == '__main__':
    initialize_db()