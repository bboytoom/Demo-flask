from marshmallow import Schema

from .utilities_schema import password_field, email_field


class UserAuthorize(Schema):

    class Meta:
        ordered = True
        name = 'user'
        plural_name = 'users'

    email = email_field
    password = password_field
