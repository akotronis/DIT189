from datetime import datetime
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
        """
        Delete in specific order to avoid Foreign key errors
        """
        UsersMarriages.query.delete()
        UsersDivorces.query.delete()
        Divorce.query.delete()
        Marriage.query.delete()
        User.query.delete()

    @classmethod
    def get_or_create_user(cls, **kwargs):
        user = User.query.filter_by(**kwargs).first()
        if not user:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
        return user
    
    @classmethod
    def get_users(cls, **kwargs):
        users = User.query
        if (role_list := kwargs.pop('role', [])):
            # Make sure role_list is a list of enum types
            role_list = [role_list] if isinstance(role_list, str) else role_list
            if isinstance(next(iter(role_list), None), str):
                role_list = User.Types.filter_keys(role_list)
            users = users.filter(User.role.in_(role_list))
        return users.filter_by(**kwargs)
    
    @classmethod
    def make_users(cls):
        for i in range(1, 31):
            num = f'{i}'.zfill(2)
            vat_num = 1000 + i
            user_data = {
                'vat_num':vat_num,
                'email':f'person{num}@gmail.com',
                'username':f'person{num}',
                'first_name':f'first_name{num}',
                'last_name':f'first_name{num}',
                'role':random.choice(User.Types.names)
            }
            cls.get_or_create_user(**user_data)
    
    @staticmethod
    def get_marriages(**kargs):
        """
        Fetch active marriages for selection to start divorce process
        """
        return Marriage.query.filter_by(**kargs)

    @classmethod
    def make_marriages(cls):
        spouses = User.query.filter(User.role==User.Types.SPOUSE).all()
        couples = [spouses[i:i + 2] for i in range(0, len(spouses), 2)]
        couples = [x for x in couples if len(x) == 2]
        for spouse_1, spouse_2 in couples:
            marriage = Marriage(start_date=cls.random_date(), in_use=True)
            spouse_1.marriages.append(marriage)
            spouse_2.marriages.append(marriage)
            db.session.add(marriage)
        db.session.commit()

    @staticmethod
    def update_marriages(filter_on_dict, values_dict):
        values_dict = {getattr(Marriage, k, None): v for k,v in values_dict.items()}
        Marriage.query.filter_by(**filter_on_dict).update(values_dict, synchronize_session=False)
        db.session.commit()

    @classmethod
    def get_divorces(cls, **kwargs):
        divorces = Divorce.query
        if (status_list := kwargs.pop('status', [])):
            # Make sure status_list is a list of enum types
            status_list = [status_list] if isinstance(status_list, str) else status_list
            if isinstance(next(iter(status_list), None), str):
                status_list = Divorce.Status.filter_keys(status_list)
            divorces = divorces.filter(Divorce.status.in_(status_list))
        return divorces.filter_by(**kwargs)
    
    @staticmethod
    def start_divorce(marriage, lawyer_email):
        # Divorce data
        data = {
            'marriage_id': marriage.id,
            'status':Divorce.Status.WAIT_LAWYER_2,
            'start_date': datetime.now().date()
        }
        divorce = Divorce(**data)
        db.session.add(divorce)
        db.session.commit()

        # Lawyer data
        lawyer = DataBase.get_users(email=lawyer_email).first()
        # Add lawyer to users_divorces
        lawyer_divorce = UsersDivorces(user_id=lawyer.id, divorce_id=divorce.id, user_role='INITIAL_LAWYER', confirmed=True)
        db.session.add(lawyer_divorce)
        # Add spouces to users_divorces
        for spouce in marriage.users:
            spouce_divorce = UsersDivorces(user_id=spouce.id, divorce_id=divorce.id, user_role='SPOUSE', confirmed=False)
            db.session.add(spouce_divorce)
        db.session.commit()
        return divorce

    @classmethod
    def initialize(cls):
        # Clear tables contents
        cls.clean_tables()

        # Create users
        cls.make_users()

        # Create marriages
        cls.make_marriages()