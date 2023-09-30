from flask import Blueprint
from src.views.url_test import url_test


generals = Blueprint('generals', __name__,  url_prefix='/api/v1')
generals.route('/ping', methods=['GET'])(url_test)
