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
        Delete table content in specific order to avoid Foreign key errors
        """
        UsersMarriages.query.delete()
        UsersDivorces.query.delete()
        Divorce.query.delete()
        Marriage.query.delete()
        User.query.delete()

    @staticmethod
    def drop_tables():
        db.drop_all()

    @staticmethod
    def drop_table(model):
        if DataBase.table_exists(model):
            model.__table__.drop()

    @classmethod
    def table_exists(cls, model):
        """
        Determine if the table of a model exists
        """
        table_names = [table.name for table in db.get_tables_for_bind()]
        return model.__tablename__ in table_names
    
    @classmethod
    def table_is_empty(cls, model):
        """
        Determine if the table of a model exists and is empty
        """
        return DataBase.table_exists(model) and not model.query.first() 

    @classmethod
    def initialize(cls, fresh=False, drop=False):
        """
        Populate database tables if they are empty.
        If fresh=True, clean them first to ensure population
        """
        if drop:
            fresh = False
            DataBase.drop_tables()
            DataBase.create_tables()

        # Clear tables contents
        if fresh:
            cls.clean_tables()

        if DataBase.table_is_empty(User):
            # Create users
            cls.make_users()

            # Create marriages
            cls.make_marriages()

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
            role_list = role_list if isinstance(role_list, list) else [role_list]
            if isinstance(next(iter(role_list), None), str):
                role_list = User.Types.filter_keys(role_list)
            users = users.filter(User.role.in_(role_list))
        return users.filter_by(**kwargs)
    
    @classmethod
    def make_users(cls):
        """
        Create 30 users of random roles
        """
        for i in range(1, 31):
            num = f'{i}'.zfill(2)
            vat_num = 1000 + i
            user_data = {
                'vat_num':vat_num,
                'email':f'person{num}@gmail.com',
                'username':f'person{num}',
                'first_name':f'first_name{num}',
                'last_name':f'last_name{num}',
                'role':random.choice(User.Types.names)
            }
            cls.get_or_create_user(**user_data)
    
    @staticmethod
    def get_marriages(**kargs):
        """
        Fetch marriages according to kwarg filters
        """
        return Marriage.query.filter_by(**kargs)

    @classmethod
    def make_marriages(cls):
        """
        Create random marriages between pairs of spouse role users
        """
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
        """
        Select marriages based of filter_on_dict and
        Update according to values_dict
        """
        values_dict = {getattr(Marriage, k, None): v for k,v in values_dict.items()}
        Marriage.query.filter_by(**filter_on_dict).update(values_dict, synchronize_session=False)
        db.session.commit()

    @classmethod
    def get_divorces(cls, **kwargs):
        """
        Get divorces according to kwargs filter dict
        """
        divorces = Divorce.query
        if (status_list := kwargs.pop('status', [])):
            # Make sure status_list is a list of enum types
            status_list = [status_list] if isinstance(status_list, str) else status_list
            if isinstance(next(iter(status_list), None), str):
                status_list = Divorce.Status.filter_keys(status_list)
            divorces = divorces.filter(Divorce.status.in_(status_list))
        return divorces.filter_by(**kwargs)
    
    @classmethod
    def add_users_divorces(**kwargs):
        db.session.add(UsersDivorces(**kwargs))
        db.session.commit()
    
    @staticmethod
    def start_divorce(marriage, lawyer_email, other_lawyer, notary):
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
        
        DataBase.add_users_divorces(
            user_id=lawyer.id, divorce_id=divorce.id, user_role=UsersDivorces.UserRole.INITIAL_LAWYER.name, confirmed=True
        )
        # Add other lawyer to users_divorces
        DataBase.add_users_divorces(
            user_id=other_lawyer.id, divorce_id=divorce.id, user_role=UsersDivorces.UserRole.SECONDARY_LAWYER.name, confirmed=False
        )
        # Add notary to users_divorces
        DataBase.add_users_divorces(
            user_id=notary.id, divorce_id=divorce.id, user_role=UsersDivorces.UserRole.NOTARY.name, confirmed=False
        )
        # Add spouses to users_divorces
        for spouse in marriage.users:
            DataBase.add_users_divorces(
                user_id=spouse.id, divorce_id=divorce.id, user_role=UsersDivorces.UserRole.SPOUSE.name, confirmed=False
            )
        return divorce
    
    @staticmethod
    def update_divorce(**kwargs):
        divorce_id = kwargs.pop('id', None)
        
        confirm = kwargs.pop('confirm', None)
        values_dict = {getattr(Divorce, k, None): v for k,v in kwargs.items() if v}
        Divorce.query.filter_by(id=divorce_id).update(values_dict, synchronize_session=False)

        db.session.commit()
        divorce = DataBase.get_divorces(id=divorce_id)
        return divorce
    
    @classmethod
    def time_elapsed_from_10day_start(cls, divorce):
        """
        Return the difference in days between the divorce start day and now
        """
        if not divorce.start_10day_date:
            return 0
        return (datetime.now().date() - divorce.start_10day_date).days
    
    @classmethod
    def confirmed_divorce_new_status(cls, divorce, user):
        """
        Input:
            - The existing divorce that is being updated
            - The user confirming the divorce
        Output: The update divorce status
        """
        user_role = user.role.name
        
        if user_role == User.Types.NOTARY.name:
            return Divorce.Status.COMPLETED
        
        user_confirmations = divorce.user_confirmations.filter_by(confirmed=True).all()
        roles_confirmed = [row.user_role.name for row in user_confirmations]
        cnt_spouses = roles_confirmed.count(User.Types.SPOUSE.name)
        
        if user_role == User.Types.LAWYER.name:
            return Divorce.Status.WAIT_SPOUSE_1
        elif user_role == User.Types.SPOUSE.name:
            if cnt_spouses == 0:
                return Divorce.Status.WAIT_SPOUSE_2
            else:
                return Divorce.Status.WAIT_10DAYS

    @classmethod
    def user_can_confirm(cls, divorce, user):
        """
        Given a divorce and a loggedin user, determine
        if the user can confirm the divorce based on it's role 
        and the divorce status
        """
        user_role, user_email = user.role.name, user.email
        user_confirmations = divorce.user_confirmations.filter_by(confirmed=True).all()
        emails_confirmed = [user_divorce.user.email for user_divorce in user_confirmations]
        cnt_emails_confirmed = len(emails_confirmed)
        if user_role == User.Types.NOTARY.name:
            return cnt_emails_confirmed == 4
        elif user_role == User.Types.SPOUSE.name:
            return all([
                cnt_emails_confirmed in [2,3],
                user_email not in emails_confirmed
            ])
        elif user_role == User.Types.LAWYER.name:
            return all([
                cnt_emails_confirmed == 1,
                user_email not in emails_confirmed
            ])
        
    @classmethod
    def user_can_cancel(cls, divorce, user):
        """
        Given a divorce and a loggedin user, determine
        if the user can cancel the divorce based on it's role 
        and the divorce status
        """
        if DataBase.time_elapsed_from_10day_start(divorce) > 10:
            divorce.status = Divorce.Status.WAIT_NOTARY
            db.session.commit()
        divorce_status = divorce.status.name
        if any([
            divorce_status in [Divorce.Status.COMPLETED.name, Divorce.Status.CANCELLED.name],
            all([
                user.role.name == User.Types.SPOUSE.name,
                divorce_status == Divorce.Status.WAIT_NOTARY.name,
            ]) 
        ]):
            return False
        return True
