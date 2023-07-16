from marshmallow import Schema, fields


class RefreshInputSchema(Schema):
    """
    Clean tables and repopulate them
    Validates inputs of the form
    - ?drop=True/False to drop tables and recreate them
    """
    drop = fields.Boolean(required=True, default=False)