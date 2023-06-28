import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db

class UsersDivorces(db.Model):

    class UserRole(enum.Enum):
        INITIAL_LAWYER = 1
        SECONDARY_LAWYER = 2
        SPOUSE = 3
        NOTARY = 4

        @classmethod
        @property
        def names(cls):
            """
            Return class attributes names as strings
            """
            return list(cls.__members__.keys())
        
        @classmethod
        @property
        def values(cls):
            """
            Return class attributes as enum types
            """
            return list(cls.__members__.values())
        
        @classmethod
        def filter_keys(cls, names=None, output='types'):
            """
            Filter by values in a names list like ['spouse', 'notary'] case insensitive
            and return:
            output='names' -> names (list of str)
            output='types' -> enum types (list o enum types)
            output='both' -> both (list of tuples (str, enum type))
            """
            names = list(map(lambda x: x.upper(), names or []))
            result = []
            for name, v in cls.__members__.items():
                if name  in names:
                    if output == 'names':
                        item = name
                    elif output == 'types':
                        item = v
                    else:
                        item = (name, v)
                    result.append(item)
            return result

    __tablename__ = 'users_divorces'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    divorce_id = db.Column(UUID(as_uuid=True), db.ForeignKey('divorces.id'), primary_key=True)
    user_role = db.Column(Enum(UserRole))
    confirmed = db.Column(db.Boolean)