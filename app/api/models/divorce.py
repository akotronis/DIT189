import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db


class Divorce(db.Model):

    class Status(enum.Enum):
        STARTED = 1 # Is it needed? It is the same with 2
        WAIT_LAWYER_2 = 2
        WAIT_SPOUSES = 3
        WAIT_10DAY = 4
        WAIT_NOTARY = 5
        COMPLETED = 6
        CANCELLED = 7

    __tablename__ = 'divorces'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marriage_id = db.Column(UUID(as_uuid=True), db.ForeignKey('marriages.id'))
    status = db.Column(Enum(Status), nullable=True)
    cancelled_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    aggrement_text = db.Column(db.String, nullable=True)
    marriage = db.relationship('Marriage', back_populates='divorces')
    users = db.relationship('User', back_populates='divorces', secondary='users_divorces')

    def __repr__(self):
        return f'<User "{self.email}">'
