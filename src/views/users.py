import logging

from flask import jsonify, abort
from flask.views import MethodView

from src.schemas.user_schema import UserSchema
from src.services.users_service import UserService
from src.views.decorators.endpoint_validation_body import validator_body


class Users(MethodView):
    """
    Endpoint for user information management
    """

    @validator_body(UserSchema)
    def post(self, data):
        try:
            user = UserService.create(data)
        except Exception as e:
            logging.error(f'Insert user error: {e}')

            return abort(500, 'Error inserting data')

        return jsonify(
            message='Successful request',
            user_uuid=user.get('uuid')
            ), 201

    def get(self):
        print('hi')

        return jsonify(
            data={}
            ), 200
