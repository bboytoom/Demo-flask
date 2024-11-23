from marshmallow import Schema, fields, validate


class UserEmailSchema(Schema):

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
