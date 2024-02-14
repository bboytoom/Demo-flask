from marshmallow import Schema, \
    fields, \
    validate, \
    validates, \
    ValidationError


class CreateUserSchema(Schema):

    class Meta:
        ordered = True

    web_identifier = fields.UUID(
        required=True
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

    @validates('name')
    def is_valid_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The name is invalid')


serializer_user_schema = CreateUserSchema()
