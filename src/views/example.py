from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from src.schemas import ExampleSchema
from src.services import ExampleService
from src.decorators import validate_token_user, validator_body


class Example(MethodView):
    """
    Endpoint for user information management
    """

    decorators = [jwt_required()]

    @validate_token_user(cls=True)
    def get(self, _user_uuid):
        ExampleService.retrieve(_user_uuid)

        return jsonify(
            message='Successful request',
            ), 200

    @validate_token_user(cls=True)
    @validator_body(ExampleSchema, cls=True)
    def post(self, _data, *args):
        # user_uuid: args[0][1]

        ExampleService.create(_data)

        return jsonify(
            message='Successful request',
            ), 200
