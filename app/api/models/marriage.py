import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db


class Marriage(db.Model):

    __tablename__ = 'marriages'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)
    in_use = db.Column(db.Boolean)
    users = db.relationship('User', back_populates='marriages', secondary='users_marriages')
    divorces = db.relationship('Divorce', back_populates='marriage', lazy='dynamic')

    def __repr__(self):
        return f'<Marriage "{self.id}">'



