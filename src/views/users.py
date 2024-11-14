from flask import jsonify
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

    @validate_token_user(AuthService, cls=True)
    def get(self, _user):
        return jsonify(
            message='Successful request',
            data=_user
            ), 200

    @validate_token_user(AuthService, cls=True)
    @validator_body(UserUpdateSchema, cls=True)
    def patch(self, _user, *args):
        user = UserService.update_info(args[0]['uuid'], _user)

        return jsonify(
            message='Successful request',
            data=user
            ), 200

    @validate_token_user(AuthService, cls=True)
    def delete(self, _user):
        token = get_jwt()

        jti = token['jti']
        ttype = token['type']

        UserService.remove(_user)
        AuthService.remove_access_user(jti, ttype)

        return '', 204
