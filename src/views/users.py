from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity


class Users(MethodView):
    """
    Endpoint for user information management
    """

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
