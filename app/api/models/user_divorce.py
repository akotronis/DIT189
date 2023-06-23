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

    __tablename__ = 'users_divorces'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    divorce_id = db.Column(UUID(as_uuid=True), db.ForeignKey('divorces.id'), primary_key=True)
    user_role = db.Column(Enum(UserRole))
    confirmed = db.Column(db.Boolean)