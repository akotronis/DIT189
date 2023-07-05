from marshmallow import Schema, fields

from ..models import Divorce


class DivorceNoMarriageSchema(Schema):
    class Meta:
        ordered = True
    id = fields.UUID()
    status = fields.Enum(Divorce.Status)
    cancelled_by = fields.Nested('UserSchema', allow_null=True, default={})
    start_date = fields.DateTime('%Y-%m-%d')
    end_date = fields.DateTime('%Y-%m-%d')
    aggrement_text = fields.Str()


class DivorceSchema(DivorceNoMarriageSchema):
    class Meta:
        ordered = True
    marriage = fields.Nested('MarriageSchema')
    users = fields.List(fields.Nested('UserSchema'))
    user_confirmations = fields.List(fields.Nested('UserConfirmationsSchema'))


class DivorceInputSchema(Schema):
    """
    Validates inputs of the form
    - ?status=COMPLETED&status=CANCELLED single or multiple (optional)
    - ?self=True/False to include only divorces(cases) wher user is involved (optional)
    """
    status = fields.List(fields.Enum(Divorce.Status), required=True)
    self = fields.Boolean(required=True)


class DivorceInputUpdateSchema(Schema):
    """
    Validates inputs of the form
    - ?confirm=True/False to declare approval or not from the request user
    """
    confirm = fields.Boolean(required=True)
    
    
class DivorceCreateSchema(Schema):
    class Meta:
        ordered = True
    marriage_id = fields.UUID()
    notary_id = fields.UUID()
    other_lawyer_id = fields.UUID()


class DivorceUpdateSchema(Schema):
    class Meta:
        ordered = True
    aggrement_text = fields.Str()