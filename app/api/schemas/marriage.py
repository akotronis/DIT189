from marshmallow import Schema, fields


class MarriageSchema(Schema):
    class Meta:
        ordered = True
    id = fields.UUID()
    start_date = fields.DateTime('%Y-%m-%d')
    end_date = fields.DateTime('%Y-%m-%d')
    in_use = fields.Boolean()


class MarriageUserDivorceSchema(MarriageSchema):
    class Meta:
        ordered = True
    users = fields.List(fields.Nested('UserSchema'))
    divorces = fields.List(fields.Nested('DivorceNoMarriageSchema'))


class MarriageInputSchema(Schema):
    """
    Validates input of the form ?in_use=True/False
    """
    in_use = fields.Boolean()