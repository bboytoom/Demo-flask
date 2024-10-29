import logging

from flask import jsonify, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

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

    @jwt_required()
    def get(self, user_uuid):
        current_user = get_jwt_identity()

        print('\n --------------------\n')
        print(user_uuid, 'uuid')
        print('\n --------------------\n')
        print(current_user, 'token')
        print('\n --------------------\n')

        return jsonify(
            data={}
            ), 200
