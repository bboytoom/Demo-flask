import re

from marshmallow import fields, validate, ValidationError

email_field = fields.Email(
    load_only=True,
    required=True,
    validate=[
        validate.Length(min=8, max=70)
        ]
    )

password_field = fields.Str(
    load_only=True,
    required=True,
    validate=[
        validate.Length(min=8, max=30)
        ]
    )


def validate_password(value):
    errors = []

    if not re.search(r"[A-Z]", value):
        errors.append('The password must have at least one capital letter.')

    if not re.search(r"[a-z]", value):
        errors.append('The password must have at least one lowercase letter.')

    if not re.search(r"[0-9]", value):
        errors.append('The password must have at least one number.')

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        errors.append('The password must have at least one special character.')

    if len(errors) != 0:
        raise ValidationError(errors)
