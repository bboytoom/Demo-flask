from flask import jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.decorators import validator_body
from src.schemas import UserSchema, UserAuthorize
from src.services import UserService, AuthService


@validator_body(UserSchema)
def sing_up(_data):
    user = UserService.create(_data)

    if user.get('code', None) == 409:
        return abort(409, 'The user does exists')

    return jsonify(
        message='Successful request',
        user_uuid=user.get('uuid')
        ), 201


@validator_body(UserAuthorize)
def login(_data):
    auth = AuthService.authorize(_data)

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

    auth = AuthService.get_new_token(email)
    auth.pop('authorize')

    return jsonify(
        message='Successful request',
        data=auth
        ), 200
