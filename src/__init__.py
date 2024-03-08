import os

from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

load_dotenv('.env')

migrate = Migrate()
marshmallow = Marshmallow()


def create_app():
    from src.config import db, config
    from src.routes import users, generals

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[os.environ.get('ENV')])

    CORS(app)

    # Database
    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)

    # Routes
    app.register_blueprint(users)
    app.register_blueprint(generals)

    # Routes error
    register_error(app)

    return app


# Handle error
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
