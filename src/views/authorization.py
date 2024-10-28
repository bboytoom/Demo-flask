import logging

from flask import jsonify, abort
from flask.views import MethodView

from src.schemas.user_authorize import UserAuthorize
from src.services.users_service import UserService
from src.views.decorators.endpoint_validation_body import validator_body


class Authorization(MethodView):
    """
    Endpoint to authorize a user in the app
    """

    @validator_body(UserAuthorize)
    def post(self, data):
        try:
            auth = UserService.authorize(data)
        except Exception as e:
            logging.error(f'authorize error: {e}')

            return abort(500, 'Error authorize')

        if not auth.get('authorize', False):
            return abort(401, 'Error in password or email')

        auth.pop('authorize')

        return jsonify(
            message='Successful request',
            data=auth
            ), 200
