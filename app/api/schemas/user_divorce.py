from marshmallow import Schema, fields

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..models import UsersDivorces


class UserConfirmationsSchema(Schema):
    # https://swagger.io/docs/specification/data-models/data-types/
    class Meta:
        ordered = True
    user_id = fields.UUID()
    user_role = fields.Enum(UsersDivorces.UserRole)
    confirmed = fields.Boolean()
    can_confirm = fields.Method('get_can_confirm', type='boolean')
    can_cancel = fields.Method('get_can_cancel', type='boolean')

    def get_can_confirm(self, obj):
        user = DataBase.get_users(id=obj.user_id).first()
        divorce = DataBase.get_divorces(id=obj.divorce_id).first()
        return DataBase.user_can_confirm(divorce, user)
    
    def get_can_cancel(self, obj):
        user = DataBase.get_users(id=obj.user_id).first()
        divorce = DataBase.get_divorces(id=obj.divorce_id).first()
        return DataBase.user_can_cancel(divorce, user)