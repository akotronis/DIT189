import random
from datetime import datetime, timedelta
from .db import db

from .models import *


class DataBase:

    @staticmethod
    def random_date():
        start = datetime.strptime('1/1/2023', '%d/%m/%Y')
        end = datetime.strptime('12/12/2023', '%d/%m/%Y')
        delta = end - start
        random_day = random.randrange(delta.days)
        return (start + timedelta(days=random_day)).date()

    @staticmethod
    def create_tables():
        # Create tables IF NOT EXIST
        db.create_all()

    @staticmethod
    def clean_tables():
        User.query.delete()
        Marriage.query.delete()
        UsersMarriages.query.delete()

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

    def make_couples(self):
        spouses = list(db.session.query(User).filter(User.role==User.Types.SPOUSE))
        couples = [spouses[i:i + 2] for i in range(0, len(spouses), 2)]
        couples = [x for x in couples if len(x) == 2]
        for spouse_1, spouse_2 in couples:
            marriage = Marriage(start_date=self.random_date())
            spouse_1.marriages.append(marriage)
            spouse_2.marriages.append(marriage)
            db.session.add(marriage)
        db.session.commit()

    def make_users(self):
        for i in range(1, 31):
            num = f'{i}'.zfill(2)
            vat_num = 1000 + i
            user_data = {
                'vat_num':vat_num,
                'email':f'person{num}@gmail.com',
                'username':f'person{num}',
                'first_name':f'first_name{num}',
                'last_name':f'first_name{num}',
                'role':random.choice(list(User.Types.__members__.keys()))
            }
            self.get_or_create(User, **user_data)

    def initialize(self):
        # Clear tables contents
        DataBase.clean_tables()

        # Create users
        self.make_users()

        # Create marriages
        self.make_couples()