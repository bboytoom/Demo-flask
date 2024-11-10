from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from src.services import AuthService
from src.decorators import validate_token_user


class Users(MethodView):
    """
    Endpoint for user information management
    """

    decorators = [jwt_required()]

    @validate_token_user(AuthService, cls=True)
    def get(self, user):
        return jsonify(data=user), 200
