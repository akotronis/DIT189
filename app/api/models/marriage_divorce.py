import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from ..db import db

class MarriagesDivorces(db.Model):

    class Status(enum.Enum):
        IN_PROGRESS = 1
        COMPLETED = 2
        CANCELLED = 3

    __tablename__ = 'marriages_divorces'
    marriage_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    divorce_id = db.Column(UUID(as_uuid=True), db.ForeignKey('divorces.id'), primary_key=True)
    status = db.Column(Enum(Status))