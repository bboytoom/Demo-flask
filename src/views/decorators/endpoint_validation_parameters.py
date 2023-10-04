import functools

from flask import abort
from src.models.User import User


def validate_user_identifier(func):
    """
    Decorator function that validates the user identifier.
    """

    @functools.wraps(func)
    def wrapper(self, **kwargs):
        identifier = kwargs.get('identifier', None)

        if not identifier:
            abort(404, 'The user does not exists')

        exists = User.retrieve_user(str(identifier))

        return func(self, exists)

    return wrapper
