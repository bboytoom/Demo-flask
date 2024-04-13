from marshmallow import Schema, fields, validate, validates, ValidationError
from src.models.user import User


class StockRegisterSchema(Schema):

    class Meta:
        ordered = True

    user_uuid = fields.UUID(required=True)

    symbol_stock = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=20)
            ]
        )

    @validates('user_uuid')
    def validate_schema(self, value):
        exists_user = User.search_user(value)

        if not exists_user:
            raise ValidationError('The user_uuid does not exists.')

        return value
