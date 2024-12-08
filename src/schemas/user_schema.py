from marshmallow import Schema, fields, validate, validates, ValidationError

from .utilities_schema import password_field, validate_password


class UserSchema(Schema):

    class Meta:
        ordered = True
        name = 'user'
        plural_name = 'users'

    uuid = fields.UUID(dump_only=True)

    email = fields.Email(
        required=True,
        validate=[
            validate.Length(min=8, max=70)
            ]
        )

    password = password_field

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

    @validates('password')
    def is_valid_password(self, value):
        validate_password(value)

        return value


user_response = UserSchema(only=('uuid', 'email', 'name', 'last_name',
                                 'birth_day', 'created_at', 'updated_at',))

user_info_response = UserSchema(only=('uuid', 'name', 'last_name', 'birth_day',))
create_user_response = UserSchema(only=('uuid',))
email_user_response = UserSchema(only=('uuid', 'email',))
