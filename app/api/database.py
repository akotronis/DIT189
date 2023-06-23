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
        Divorce.query.delete()
        UsersDivorces.query.delete()

    def get_or_create_user(self, **kwargs):
        email = kwargs.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
        return user

    def make_marriages(self):
        spouses = list(User.query.filter(User.role==User.Types.SPOUSE))
        couples = [spouses[i:i + 2] for i in range(0, len(spouses), 2)]
        couples = [x for x in couples if len(x) == 2]
        for spouse_1, spouse_2 in couples:
            marriage = Marriage(start_date=self.random_date(), in_use=True)
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
            self.get_or_create_user(**user_data)

    @staticmethod
    def get_active_marriages():
        '''Fetch active marriages for selection to start divorce process'''
        # TODO: Specify Data Format
        print([m.users for m in Marriage.query.filter_by(in_use=True).all()])

    @staticmethod
    def start_divorce(marriage_id):
        ...

    def initialize(self):
        # Clear tables contents
        DataBase.clean_tables()

        # Create users
        self.make_users()

        # Create marriages
        self.make_marriages()