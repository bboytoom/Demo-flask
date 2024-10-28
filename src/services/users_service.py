import os
import bcrypt
import logging

from src.schemas.user_schema import create_user_response, authorize_user_response
from src.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    @classmethod
    def authorize(cls, _data: dict) -> dict:

        try:
            user = UserRepository.get_by_email(_data.get('email', None))

            if not cls._verify_password(_data.get('password', None), user.password_hash):
                return {
                    'authorize': False
                    }

            credentials = authorize_user_response.dump(user)
            credentials.update({
                'authorize': True
                })

            return credentials
        except Exception as e:
            logging.error(f'Error authorize: {e}')

    @classmethod
    def create(cls, _data: dict) -> dict:
        try:
            _data['password'] = cls._hash_password(_data.get('password'))

            return create_user_response.dump(UserRepository.add(_data))
        except Exception as e:
            logging.error(f'Error create_user: {e}')

    @staticmethod
    def _hash_password(_password: str) -> str:
        combined_password = _password + os.environ.get('SECRET_KEY')

        password_bytes = combined_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode('utf-8')

    @staticmethod
    def _verify_password(_password: str, _hashed_password: str) -> bool:
        combined_password = _password + os.environ.get('SECRET_KEY')

        return bcrypt.checkpw(combined_password.encode('utf-8'), _hashed_password.encode('utf-8'))
