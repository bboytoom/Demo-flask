from flask import Blueprint
from src.views.url_test import url_test
from src.views.authorization import Authorization


generals = Blueprint('generals', __name__,  url_prefix='/api/v1')

generals.route('/ping', methods=['GET'])(url_test)
generals.add_url_rule(
    '/login',
    view_func=Authorization.as_view('login'),
    methods=['POST']
    )
