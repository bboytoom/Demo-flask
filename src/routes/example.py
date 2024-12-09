from flask import Blueprint

from src.views import Example

example = Blueprint('example', __name__,  url_prefix='/api/v1/example')

example.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Example.as_view('retrieve'),
    methods=['GET']
    )

example.add_url_rule(
    '/<uuid:user_uuid>',
    view_func=Example.as_view('post'),
    methods=['POST']
    )
