from marshmallow import Schema, fields

from ..models import Divorce

class DivorceNoMarriageSchema(Schema):
    class Meta:
        ordered = True
    id = fields.UUID()
    status = fields.Enum(Divorce.Status)
    cancelled_by = fields.Nested('UserSchema')
    start_date = fields.DateTime('%Y-%m-%d')
    end_date = fields.DateTime('%Y-%m-%d')
    aggrement_text = fields.Str()


class DivorceSchema(DivorceNoMarriageSchema):
    class Meta:
        ordered = True
    marriage = fields.Nested('MarriageSchema')


class DivorceInputSchema(Schema):
    """
    Validates inputs of the form ?status=COMPLETED&role=CANCELLED single or multiple
    """
    status = fields.List(fields.Enum(Divorce.Status))
    
    