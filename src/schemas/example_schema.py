from marshmallow import Schema, fields, validate, validates, ValidationError


class ExampleSchema(Schema):

    class Meta:
        ordered = True
        name = 'example'
        plural_name = 'examples'

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=30)
            ]
        )

    @validates('name')
    def is_valid_name(self, value):

        if value.isalnum():
            return value

        raise ValidationError('The name is invalid.')


example_response = ExampleSchema(only=('name',))
