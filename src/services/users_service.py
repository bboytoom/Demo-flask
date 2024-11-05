import os
import uuid
import bcrypt
import logging

from src.schemas import create_user_response
from src.repositories import UserRepository
from src.helpers import CryptographyMessage


class UserService:

    _user_repository = UserRepository()
    _security_field = CryptographyMessage()

    @classmethod
    def create(cls, _data: dict) -> dict:
        try:
            _data['password'] = cls._hash_password(_data.get('password'))

            _data['email'] = cls._security_field.encrypt(_data.get('email'))
            _data['name'] = cls._security_field.encrypt(_data.get('name'))
            _data['last_name'] = cls._security_field.encrypt(_data.get('last_name'))

            if _data.get('birth_day', None):
                birth_day = cls._security_field.encrypt(_data.get('birth_day'))
            else:
                birth_day = None

            _data.update({
                'uuid': uuid.uuid4(),
                'birth_day': birth_day
                })

            return create_user_response.dump(cls._user_repository.add(_data))
        except Exception as e:
            if e.args[0] == 'Duplicated data in database':
                return {
                    'code': 409
                    }

            logging.error(f'Error create_user: {e}')

    @staticmethod
    def _hash_password(_password: str) -> str:
        combined_password = _password + os.environ.get('SECRET_KEY')

        password_bytes = combined_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode('utf-8')
