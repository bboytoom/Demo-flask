from marshmallow import Schema

from .utilities_schema import email_field


class UserEmailSchema(Schema):

    class Meta:
        ordered = True
        name = 'user'
        plural_name = 'users'

    email = email_field
