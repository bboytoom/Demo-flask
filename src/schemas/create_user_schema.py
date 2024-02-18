from marshmallow import Schema, \
    fields, \
    validate, \
    validates, \
    ValidationError

from src.models.User import User


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

    @validates('last_name')
    def is_valid_last_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The last_name is invalid')

    @validates('web_identifier')
    def is_unique_web_identifier(self, value):
        search_web_identifier = User.retrieve_user(str(value), False)

        if search_web_identifier:
            raise ValidationError('The web_identifier must be unique.')

        return value


serializer_user_schema = CreateUserSchema()
