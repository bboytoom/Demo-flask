from flask import Blueprint

from src.views import url_test, sing_up, login, refresh


generals = Blueprint('generals', __name__,  url_prefix='/api/v1')

# Test
generals.route('/ping', methods=['GET'])(url_test)

# Authorizer
generals.route('/sing_up', methods=['POST'])(sing_up)
generals.route('/login', methods=['POST'])(login)
generals.route('/refresh', methods=['POST'])(refresh)
