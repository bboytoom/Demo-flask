import logging

from flask import jsonify, abort
from flask.views import MethodView

from src.models.User import User
from src.views.decorators.endpoint_validation_body import validator_body
from src.views.decorators.endpoint_validation_parameters import validate_user_identifier

from src.schemas.create_user_schema import CreateUserSchema, \
    serializer_user_schema


class Users(MethodView):
    """
    Endpoint for user information management
    """

    @validate_user_identifier
    def get(self, user):
        return jsonify(serializer_user_schema.dump(user)), 200

    @validator_body(CreateUserSchema)
    def post(self, data):
        user = User.new_user(data)

        try:
            user.save()
        except Exception as e:
            logging.error(f'Insert User History error: {e}')

            return abort(500, 'Error inserting data')

        return jsonify(
            message='Successful request',
            user_uuid=user.uuid
            ), 201
