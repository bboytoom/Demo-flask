import re

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):

    class Meta:
        ordered = False
        name = 'user'
        plural_name = 'users'

    uuid = fields.UUID(dump_only=True)

    email = fields.Email(
        required=True,
        validate=[
            validate.Length(min=8, max=70)
            ]
        )

    password_hash = fields.Str(
        load_only=True,
        data_key='password',
        required=True,
        validate=[
            validate.Length(min=8, max=30)
            ]
        )

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

        raise ValidationError('The name is invalid.')

    @validates('last_name')
    def is_valid_last_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The last_name is invalid.')

    @validates('password_hash')
    def is_valid_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise ValidationError('The password must have at least one capital letter.')

        if not re.search(r"[a-z]", value):
            raise ValidationError('The password must have at least one lowercase letter.')

        if not re.search(r"[0-9]", value):
            raise ValidationError('The password must have at least one number.')

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError('The password must have at least one special character.')

        return value


create_user_response = UserSchema(only=('uuid',))
authorize_user_response = UserSchema(only=('uuid', 'name', 'last_name', 'birth_day',))
