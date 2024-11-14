import os
import uuid
import bcrypt
import logging

from datetime import datetime

from src.schemas import create_user_response, user_info_response
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
                'birth_day': birth_day,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
                })

            return create_user_response.dump(cls._user_repository.add(_data))
        except Exception as e:
            if e.args[0] == 'Duplicated data in database':
                return {
                    'code': 409
                    }

            logging.error(f'Error create_user: {e}')

    @classmethod
    def update_info(cls, _user_uuid, _data: dict) -> dict:
        try:
            _data['name'] = cls._security_field.encrypt(_data.get('name'))
            _data['last_name'] = cls._security_field.encrypt(_data.get('last_name'))

            if _data.get('birth_day', None):
                birth_day = cls._security_field.encrypt(_data.get('birth_day'))
            else:
                birth_day = None

            _data.update({
                'birth_day': birth_day,
                'updated_at': datetime.now()
                })

            user = cls._user_repository.update_user(_user_uuid, _data)

            user.uuid = _user_uuid
            user.name = cls._security_field.decrypt(user.name)
            user.last_name = cls._security_field.decrypt(user.last_name)

            if user.birth_day:
                birth_day_decrypt = cls._security_field.decrypt(user.birth_day)
                user.birth_day = datetime.strptime(birth_day_decrypt, '%Y-%m-%d')

            return user_info_response.dump(user)
        except Exception as e:
            logging.error(f'Error update: {e}')

    @classmethod
    def remove(cls, _data: dict) -> None:
        remove_data = {
            'deleted_at': datetime.now()
            }

        try:
            return cls._user_repository.remove_user(_data.get('uuid'), remove_data)
        except Exception as e:
            logging.error(f'Error remove: {e}')

    @staticmethod
    def _hash_password(_password: str) -> str:
        combined_password = _password + os.environ.get('SECRET_KEY')

        password_bytes = combined_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode('utf-8')
