from flask import Blueprint

from src.views import Users, change_password, change_email

users = Blueprint('users', __name__,  url_prefix='/api/v1/users')

users.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Users.as_view('user_by_uuid'),
    methods=['GET']
    )

users.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Users.as_view('update_user'),
    methods=['PATCH']
    )

users.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Users.as_view('remove_user'),
    methods=['DELETE']
    )


users.route('/<uuid:user_uuid>/change-email', methods=['PATCH'])(change_email)
users.route('/<uuid:user_uuid>/change-password', methods=['PATCH'])(change_password)
