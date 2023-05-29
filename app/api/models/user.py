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

    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vat_num = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String, default='NA')
    last_name = db.Column(db.String, default='NA')
    role = db.Column(Enum(Types))
    marriages = db.relationship('Marriage', back_populates='users', secondary='users_marriages')

    def __repr__(self):
        return f'<User "{self.email}">'



