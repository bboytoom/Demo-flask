import functools

from flask import request, abort
from flask_jwt_extended import get_jwt_identity


def validate_token_user(cls=False):
    """
    Decorator function that validates token and user_uuid
    """

    # Sub function
    def validation(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token_identifier = get_jwt_identity()
            user_uuid = kwargs.get('user_uuid', None)

            if token_identifier != str(user_uuid):
                return abort(404, 'The user does not exists')

            if not cls:
                return func(token_identifier)

            return func(args[0], token_identifier)
        return wrapper
    return validation


def validator_body(schema, cls=False):
    """
    Decorator function that validates the endpoint body.
    """

    # Sub function
    def validation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            content_type = request.headers.get('Content-Type')
            schema_event = schema()

            if content_type != 'application/json':
                return abort(400, 'Content-Type not supported!')

            errors = schema_event.validate(request.get_json())

            if errors:
                return abort(422, errors)

            if len(args) == 0:
                user_original = None
            else:
                user_original = args

            if not cls:
                return func(request.get_json(), user_original)

            return func(args[0], request.get_json(), user_original)
        return wrapper
    return validation
