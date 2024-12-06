import re

from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema


class UserPasswordSchema(Schema):

    password = fields.Str(
        load_only=True,
        required=True,
        validate=[
            validate.Length(min=8, max=30)
            ]
        )

    password_confirmed = fields.Str(
        load_only=True,
        required=True,
        validate=[
            validate.Length(min=8, max=30)
            ]
        )

    @validates('password')
    def validate_password(self, value):
        self._validate_password(value)

        return value

    @validates('password_confirmed')
    def validate_password_confirmed(self, value):
        self._validate_password(value)

        return value

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        if data.get('password') != data.get('password_confirmed'):
            raise ValidationError({'password_confirmed': ['Passwords must match.']})

    def _validate_password(self, value):
        errors = []

        if not re.search(r"[A-Z]", value):
            errors.append('The password must have at least one capital letter.')

        if not re.search(r"[a-z]", value):
            errors.append('The password must have at least one lowercase letter.')

        if not re.search(r"[0-9]", value):
            errors.append('The password must have at least one number.')

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            errors.append('The password must have at least one special character.')

        if len(errors) != 0:
            raise ValidationError(errors)
