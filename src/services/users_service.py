import os
import uuid
import bcrypt
import logging

from datetime import datetime

from src.schemas import (create_user_response, user_info_response, email_user_response,
                         user_response)
from src.repositories import UserRepository
from src.helpers import CryptographyMessage


class UserService:

    _user_repository = UserRepository()
    _security_field = CryptographyMessage()

    @classmethod
    def retrieve(cls, _user_uuid: str) -> dict:
        try:
            user = cls._user_repository.get_user_by_uuid(_user_uuid)

            if not user:
                return {}

            return user_response.dump(cls._user_format(user))
        except Exception as e:
            logging.error(f'Error retrieve: {e}')

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
    def update_password(cls, _user_uuid: str, _data: dict) -> None:

        update_password = {
            'password_hash': cls._hash_password(_data.get('password')),
            'updated_at': datetime.now()
            }

        cls._user_repository.update_user(_user_uuid, update_password)

        return None

    @classmethod
    def update_email(cls, _user_uuid: str, _data: dict) -> dict:
        email = cls._security_field.encrypt(_data.get('email'))
        exists_email = cls._user_repository.exists_email(_user_uuid, email)

        if exists_email:
            return {}

        user = cls._user_repository.update_user(_user_uuid, {
            'email': email,
            'updated_at': datetime.now()
            })

        user.uuid = _user_uuid
        user.email = cls._security_field.decrypt(user.email)

        return email_user_response.dump(user)

    @classmethod
    def update_info(cls, _user_uuid: str, _data: dict) -> dict:
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
    def remove(cls, _user_uuid: str) -> None:
        remove_data = {
            'deleted_at': datetime.now()
            }

        try:
            return cls._user_repository.remove_user(_user_uuid, remove_data)
        except Exception as e:
            logging.error(f'Error remove: {e}')

    @classmethod
    def _user_format(cls, _data):
        column_names = ['uuid', 'email', 'password_hash', 'name', 'last_name', 'birth_day',
                        'created_at', 'updated_at']

        data_dict = dict(zip(column_names, _data))

        data_dict['email'] = cls._security_field.decrypt(_data.email)
        data_dict['name'] = cls._security_field.decrypt(_data.name)
        data_dict['last_name'] = cls._security_field.decrypt(_data.last_name)

        if _data.birth_day:
            birth_day_decrypt = cls._security_field.decrypt(_data.birth_day)
            data_dict['birth_day'] = datetime.strptime(birth_day_decrypt, '%Y-%m-%d')

        return cls._user_repository.create_object(data_dict)

    @staticmethod
    def _hash_password(_password: str) -> str:
        combined_password = _password + os.environ.get('SECRET_KEY')

        password_bytes = combined_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode('utf-8')
