import logging

from flask import jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.schemas.user_schema import UserSchema
from src.schemas.user_authorize import UserAuthorize
from src.services.users_service import UserService
from src.views.decorators.endpoint_validation_body import validator_body


@validator_body(UserSchema)
def sing_up(_data):
    try:
        user = UserService.create(_data)
    except Exception as e:
        logging.error(f'Insert user error: {e}')

        return abort(500, 'Error inserting data')

    return jsonify(
        message='Successful request',
        user_uuid=user.get('uuid')
        ), 201


@validator_body(UserAuthorize)
def login(_data):
    try:
        auth = UserService.authorize(_data)
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


@jwt_required(refresh=True)
def refresh():
    email = get_jwt_identity()

    auth = UserService.get_new_token(email)
    auth.pop('authorize')

    return jsonify(
        message='Successful request',
        data=auth
        ), 200
