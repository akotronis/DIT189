import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db


class Marriage(db.Model):

    class DevorceStatus(enum.Enum):
        STARTED = 1
        WAIT_LAWYER_2 = 2
        WAIT_SPOUSES = 3
        WAIT_10DAY = 4
        WAIT_NOTARY = 5
        COMPLETED = 6
        CANCELLED = 7

    __tablename__ = 'marriages'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = db.Column(db.Date)
    divorce_start_date = db.Column(db.Date, nullable=True)
    divorce_status = db.Column(Enum(DevorceStatus), nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    aggrement_text = db.Column(db.String, nullable=True)
    users = db.relationship('User', back_populates='marriages', secondary='users_marriages')

    def __repr__(self):
        return f'<Marriage "{self.id}">'



