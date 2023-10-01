import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv('.env')


def create_app():
    # Config
    from src.config.sqlalchemy_db import db
    from src.routes.generals import generals
    from src.config.application import config

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[os.environ.get('ENV')])

    CORS(app)

    # Database
    db.init_app(app)

    # Routes
    app.register_blueprint(generals)

    # Routes error
    register_error(app)

    return app


def register_error(app):
    from src.helpers.handler_errors import page_not_found, \
        internal_server_error, \
        rate_limit_handler, \
        bad_request_handler, \
        method_not_allow_handler, \
        unprocessable_entity, \
        conflict_handler, \
        unauthorized, \
        forbidden

    app.register_error_handler(400, bad_request_handler)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allow_handler)
    app.register_error_handler(409, conflict_handler)
    app.register_error_handler(422, unprocessable_entity)
    app.register_error_handler(429, rate_limit_handler)
    app.register_error_handler(500, internal_server_error)
