from flask import Blueprint

from src.views.users import Users

users = Blueprint('users', __name__,  url_prefix='/api/v1/users')

users.add_url_rule(
    '',
    view_func=Users.as_view('create_user'),
    methods=['POST']
    )
