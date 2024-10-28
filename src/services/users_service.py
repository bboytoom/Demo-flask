import os
import bcrypt
import logging

from src.schemas.user_schema import create_user_response
from src.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    @classmethod
    def create(cls, _data: dict) -> dict:
        try:
            _data['password'] = cls._hash_password(_data.get('password'))

            return create_user_response.dump(UserRepository.add(_data))
        except Exception as e:
            logging.error(f'Error en create_user: {e}')

    @staticmethod
    def _hash_password(_password: str) -> str:
        password_plus = _password + os.environ.get('SECRET_KEY')

        password_bytes = password_plus.encode('utf-8')
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode('utf-8')
