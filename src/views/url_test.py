from datetime import datetime
from flask import jsonify


def url_test():
    now = datetime.now()

    return jsonify(
        result='pong',
        datetime=now.strftime('%Y-%m-%d %H:%M:%S')
        ), 200
