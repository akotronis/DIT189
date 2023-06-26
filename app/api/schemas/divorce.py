from marshmallow import Schema, fields

from ..models import Divorce

class DivorceSchema(Schema):
    class Meta:
        ordered = True
    id = fields.UUID()
    marriage = fields.Nested('MarriageSchema')
    status = fields.Enum(Divorce.Status)
    cancelled_by = fields.Nested('UserSchema')
    start_date = fields.DateTime('%Y-%m-%d')
    end_date = fields.DateTime('%Y-%m-%d')
    aggrement_text = fields.Str()
    
    