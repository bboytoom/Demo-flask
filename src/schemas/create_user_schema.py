import enum

from marshmallow import Schema, \
    fields, \
    validate, \
    validates, \
    ValidationError, \
    post_load


class TypeOnboarding(enum.Enum):
    ONBOARDING_STEP_ONE = 'ONBOARDING_STEP_ONE'
    ONBOARDING_STEP_TWO = 'ONBOARDING_STEP_TWO'


class CreateUserSchema(Schema):

    class Meta:
        ordered = True

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=25)
            ]
        )

    onboarding = fields.Enum(
        TypeOnboarding,
        validate=validate.OneOf([
            'ONBOARDING_STEP_ONE',
            'ONBOARDING_STEP_TWO'
            ])
        )

    @validates('name')
    def is_valid_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The name is invalid')

    @post_load
    def post_load(self, data, **kwargs):

        data['web_identifier'] = str(data.get('web_identifier'))
        data['onboarding'] = 'ONBOARDING_STEP_ONE'

        return data


serializer_user_schema = CreateUserSchema()
