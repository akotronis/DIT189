import random
from .db import db

from .models import User


class DataBase:

    @staticmethod
    def create_tables():
        # Create tables IF NOT EXIST
        db.create_all()

    def get_or_create(self, model, **kwargs):
        email = kwargs.get('email')
        instance = db.session.query(model).filter_by(email=email).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance

    @staticmethod
    def clean_tables():
        User.query.delete()

    def initialize(self):
        for i in range(1, 16):
            num = f'{i}'.zfill(2)
            vat_num = 1000 + i
            user_data = {
                'vat_num':vat_num,
                'email':f'person{num}@gmail.com',
                'username':f'person{num}',
                'role':random.choice(list(User.Types.__members__.keys())),
            }
            self.get_or_create(User, **user_data)