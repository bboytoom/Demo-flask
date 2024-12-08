from flask import jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from src.decorators import validator_body
from src.schemas import UserSchema, UserAuthorize
from src.services import UserService, AuthService
from src.helpers import auth


@auth.login_required
@validator_body(UserSchema)
def sing_up(_data, _):
    user = UserService.create(_data)

    if len(user) == 0:
        return abort(400, {'Sing_up': 'Error in sing_up.'})

    if user.get('code', None) == 409:
        return abort(409, 'The user does exists')

    return jsonify(
        message='Successful request',
        data={
            'uuid': user.get('uuid')
            }
        ), 201


@auth.login_required
@validator_body(UserAuthorize)
def login(_data, _):
    auth = AuthService.authorize(_data)

    if len(auth) == 0:
        return abort(422, {'Login': 'Error in password or email.'})

    return jsonify(
        message='Successful request',
        data=auth
        ), 200


@jwt_required(verify_type=False)
def logout():
    token = get_jwt()

    jti = token['jti']
    ttype = token['type']

    if not AuthService.remove_access_user(jti, ttype):
        return abort(400, 'Error in logout')

    return jsonify(
        message='Successful request'
        ), 200


@jwt_required(refresh=True)
def refresh():
    user_uuid = get_jwt_identity()

    auth = AuthService.get_new_token(user_uuid)

    if len(auth) == 0:
        return abort(422, {'Refresh': 'Error in refresh token.'})

    auth.pop('authorize')

    return jsonify(
        message='Successful request',
        data=auth
        ), 200
