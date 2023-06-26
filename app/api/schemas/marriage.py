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
    users = fields.List(fields.Nested('PlainUserSchema'))
    divorces = fields.List(fields.Nested('DivorceSchema'))