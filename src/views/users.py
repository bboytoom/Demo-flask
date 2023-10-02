from flask import jsonify
from flask.views import MethodView


class Users(MethodView):

    def get(self, identifier):
        print(identifier)

        return jsonify(
            name='name_test',
            onboarding='ONBOARDING_STEP_TWO'
            ), 200

    def post(self):
        return jsonify(
            onboarding='ONBOARDING_STEP_TWO'
            ), 201
