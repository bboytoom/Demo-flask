import logging

from flask import jsonify, abort
from flask.views import MethodView

from src.models.user import User
from src.schemas.create_user_schema import CreateUserSchema
from src.views.decorators.endpoint_validation_body import validator_body


class Users(MethodView):
    """
    Endpoint for user information management
    """

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
