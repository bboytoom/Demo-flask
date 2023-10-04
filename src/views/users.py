import logging

from flask import jsonify, abort
from flask.views import MethodView

from src.models.User import User
from src.schemas.create_user_schema import CreateUserSchema, serializer_user_schema
from src.views.decorators.endpoint_validation_body import validator_body
from src.views.decorators.endpoint_validation_parameters import validate_user_identifier


class Users(MethodView):

    @validate_user_identifier
    def get(self, user):
        return jsonify(serializer_user_schema.dump(user)), 200

    @validator_body(CreateUserSchema)
    def post(self, data):
        user = User.new_user(data)

        try:
            user.save()
        except Exception as e:
            if '1062' in e.args[0]:
                return abort(409, 'The identifier already exists')

            logging.error(f'Insert User History error: {e}')

            return abort(500, 'Error inserting data')

        return jsonify(
            onboarding='ONBOARDING_STEP_TWO'
            ), 201
