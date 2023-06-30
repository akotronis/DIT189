from marshmallow import Schema, fields

from ..models import UsersDivorces

class UserConfirmationsSchema(Schema):
    class Meta:
        ordered = True
    user_id = fields.UUID()
    user_role = fields.Enum(UsersDivorces.UserRole)
    confirmed = fields.Boolean()