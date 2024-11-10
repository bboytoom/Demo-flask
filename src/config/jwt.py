import os

from flask import jsonify, request
from flask_jwt_extended import JWTManager


class JWTConfig:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', None)
    JWT_ACCESS_TOKEN_EXPIRES = 10800
    JWT_REFRESH_TOKEN_EXPIRES = 864000
    JWT_ALGORITHM = 'HS512'


jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_payload):
    return jsonify(
        error='Unauthorized',
        exception='The token expired',
        path=request.path,
        method=request.method
        ), 401


@jwt.invalid_token_loader
def invalid_token_callback(_jwt_header, _jwt_payload):
    return jsonify(
        error='Unauthorized',
        exception='The invalid token',
        path=request.path,
        method=request.method
        ), 401


@jwt.unauthorized_loader
def unauthorized_loader_callback(_callback):
    return jsonify(
        error='Unauthorized',
        exception='Missing Authorization Header',
        path=request.path,
        method=request.method
        ), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_loader_callback(_jwt_header, _jwt_payload):
    return jsonify(
        error='Unauthorized',
        exception='You need to refresh the token',
        path=request.path,
        method=request.method
        ), 401
