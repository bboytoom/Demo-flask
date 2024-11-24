from flask import jsonify, abort
from flask_jwt_extended import jwt_required


from src.schemas import UserEmailSchema, UserPasswordSchema
from src.services import UserService
from src.decorators import validate_token_user, validator_body


@jwt_required()
@validate_token_user()
@validator_body(UserEmailSchema)
def change_email(_data: dict, *args: tuple):
    user = UserService.update_email(args[0][0], _data)

    if len(user) == 0:
        return abort(409, 'The email already exists')

    return jsonify(
        message='Successful request',
        data=user
        ), 200


@jwt_required()
@validate_token_user()
@validator_body(UserPasswordSchema)
def change_password(_data: dict, *args: tuple):
    UserService.update_password(args[0][0], _data)

    return jsonify(
        message='Successful request'
        ), 200
