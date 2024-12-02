from marshmallow import Schema, fields, validate


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
