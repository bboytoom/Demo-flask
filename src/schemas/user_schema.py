from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):

    class Meta:
        ordered = True

    uuid = fields.UUID(dump_only=True)

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=30)
            ]
        )

    last_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=70)
            ]
        )

    birth_day = fields.Date('%Y-%m-%d')

    status = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('name')
    def is_valid_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The name is invalid')

    @validates('last_name')
    def is_valid_last_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The last_name is invalid')


create_user_response = UserSchema(only=('uuid',))
