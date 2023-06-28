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


class DivorceInputSchema(Schema):
    """
    Validates inputs of the form
    - ?status=COMPLETED&role=CANCELLED single or multiple (optional)
    - ?self=True/False to include only divorces(cases) wher user is involved (optional)
    """
    status = fields.List(fields.Enum(Divorce.Status))
    self = fields.Boolean(load_default=True)
    
    
class DivorceCreateSchema(Schema):
    class Meta:
        ordered = True
    marriage_id = fields.UUID()