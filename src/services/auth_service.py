import os
import bcrypt
import logging

from flask_jwt_extended import create_access_token, create_refresh_token

from src.schemas import authorize_user_response
from src.repositories import UserRepository


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    @classmethod
    def get_new_token(cls, _email: str) -> dict:
        try:
            return cls._new_credentials(_email, None)
        except Exception as e:
            logging.error(f'Error get new token: {e}')

    @classmethod
    def authorize(cls, _data: dict) -> dict:

        try:
            return cls._new_credentials(_data.get('email'), _data.get('password'))
        except Exception as e:
            logging.error(f'Error authorize: {e}')

    @classmethod
    def _new_credentials(cls, _email: str, _password: str | None) -> dict:
        try:
            user = UserRepository.get_user_by_email(_email)

            if _password and not cls._verify_password(_password, user.password_hash):
                return {'authorize': False}

            credentials = authorize_user_response.dump(user)

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            credentials.update({
                'authorize': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': 10800,
                'token_type': 'Bearer'
                })

            return credentials
        except Exception as e:
            logging.error(f'Error new_credentials: {e}')

    @staticmethod
    def _verify_password(_password: str, _hashed_password: str) -> bool:
        combined_password = _password + os.environ.get('SECRET_KEY')

        return bcrypt.checkpw(combined_password.encode('utf-8'), _hashed_password.encode('utf-8'))
