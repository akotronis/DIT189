import uuid
from sqlalchemy.dialects.postgresql import UUID

from ..db import db

class UsersMarriages(db.Model):
    __tablename__ = 'users_marriages'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    marriage_id = db.Column(UUID(as_uuid=True), db.ForeignKey('marriages.id'), primary_key=True)