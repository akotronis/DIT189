from marshmallow import Schema, fields

from ..models import User


class UserSchema(Schema):
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
    """
    Validates inputs of the form
    - ?role=LAWYER&role=SPOUSE multiple to filter based on user roles
    - ?self=True/False to include self or not
    """
    role = fields.List(fields.Enum(User.Types), required=True)
    self = fields.Boolean(required=True)


class KeycloakUserInputSchema(Schema):
    """
    Validates inputs of the form
    - ?role=LAWYER&role=SPOUSE etc single
    """
    role = fields.Enum(User.Types, required=True)


class KeycloakUserOutputSchema(Schema):
    """
    Output of user created in Keycloak
    """
    email = fields.Email()
    # role = fields.Enum(User.Types)
    token = fields.Str()