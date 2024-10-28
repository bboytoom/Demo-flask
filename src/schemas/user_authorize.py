import re
from marshmallow import Schema, fields, validate, validates, ValidationError


class UserAuthorize(Schema):

    class Meta:
        ordered = True
        name = 'user'
        plural_name = 'users'

    email = fields.Email(
        load_only=True,
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
