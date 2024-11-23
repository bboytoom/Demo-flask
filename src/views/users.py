from flask import jsonify, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt

from src.schemas import UserUpdateSchema
from src.services import AuthService, UserService
from src.decorators import validate_token_user, validator_body


class Users(MethodView):
    """
    Endpoint for user information management
    """

    decorators = [jwt_required()]

    @validate_token_user(cls=True)
    def get(self, _user_uuid):
        user = UserService.retrieve(_user_uuid)

        if len(user) == 0:
            return abort(404, 'The user does not exists')

        return jsonify(
            message='Successful request',
            data=user
            ), 200

    @validate_token_user(cls=True)
    @validator_body(UserUpdateSchema, cls=True)
    def patch(self, _data, *args):
        user = UserService.update_info(args[0][1], _data)

        return jsonify(
            message='Successful request',
            data=user
            ), 200

    @validate_token_user(cls=True)
    def delete(self, _user_uuid):
        token = get_jwt()

        jti = token['jti']
        ttype = token['type']

        user = UserService.retrieve(_user_uuid)

        if len(user) == 0:
            return abort(404, 'The user does not exists')

        UserService.remove(_user_uuid)
        AuthService.remove_access_user(jti, ttype)

        return '', 204
