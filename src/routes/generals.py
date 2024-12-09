from flask import Blueprint

from src.views import url_test


generals = Blueprint('generals', __name__,  url_prefix='/api/v1')

# Test
generals.route('/ping', methods=['GET'])(url_test)
