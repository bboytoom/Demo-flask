from marshmallow import Schema, validates, ValidationError, validates_schema

from .utilities_schema import password_field, validate_password


class UserPasswordSchema(Schema):

    password = password_field
    password_confirmed = password_field

    @validates('password')
    def validate_password(self, value):
        validate_password(value)

        return value

    @validates('password_confirmed')
    def validate_password_confirmed(self, value):
        validate_password(value)

        return value

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        if data.get('password') != data.get('password_confirmed'):
            raise ValidationError({'password_confirmed': ['Passwords must match.']})
