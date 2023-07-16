import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db


class Divorce(db.Model):

    class Status(enum.Enum):
        WAIT_LAWYER_2 = 1
        WAIT_SPOUSE_1 = 2
        WAIT_SPOUSE_2 = 3
        WAIT_10DAYS = 4
        WAIT_NOTARY = 5
        COMPLETED = 6
        CANCELLED = 7

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
            Filter by values in a names list like ['completed', 'cancelled'] case insensitive
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

    __tablename__ = 'divorces'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marriage_id = db.Column(UUID(as_uuid=True), db.ForeignKey('marriages.id'))
    status = db.Column(Enum(Status), nullable=True)
    cancelled_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    start_date = db.Column(db.Date, nullable=True)
    start_10day_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    aggrement_text = db.Column(db.String, nullable=True)
    marriage = db.relationship('Marriage', back_populates='divorces')
    users = db.relationship('User', back_populates='divorces', secondary='users_divorces')
    user_confirmations = db.relationship('UsersDivorces', viewonly=True, lazy='dynamic')

    def __repr__(self):
        return f'<Divorce "{self.id}">'
