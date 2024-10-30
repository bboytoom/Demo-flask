from flask import Blueprint

from src.views.users import Users

users = Blueprint('users', __name__,  url_prefix='/api/v1/users')

users.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Users.as_view('user_by_uuid'),
    methods=['GET']
    )
