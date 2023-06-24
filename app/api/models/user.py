import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db


class User(db.Model):

    class Types(enum.Enum):
        SPOUSE = 1
        LAWYER = 2
        NOTARY = 3
    
        @classmethod
        @property
        def names(cls):
            return cls.__members__.keys()
        
        @classmethod
        @property
        def values(cls):
            return cls.__members__.values()
        
        @classmethod
        def filter_keys(cls, names=None, output='types'):
            """
            Filter by values in a names list like ['spouse', 'lawyer'] case insensitive
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

    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String, default='NA')
    last_name = db.Column(db.String, default='NA')
    vat_num = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    role = db.Column(Enum(Types))
    marriages = db.relationship('Marriage', back_populates='users', secondary='users_marriages')
    divorces = db.relationship('Divorce', back_populates='users', secondary='users_divorces')

    def __repr__(self):
        return f'<User "{self.email}">'



