from marshmallow import Schema, fields

from ..models import User


class UserOutputSchema(Schema):
    class Meta:
        ordered = True
    id = fields.UUID()
    first_name = fields.Str()
    last_name = fields.Str()
    vat_num = fields.Str()
    email = fields.Email()
    username = fields.Str()
    role = fields.Enum(User.Types)


class UserInputSchema(Schema):
    class Meta:
        ordered = True
    role = fields.List(fields.Enum(User.Types), required=False)