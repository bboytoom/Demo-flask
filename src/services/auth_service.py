import os
import bcrypt
import logging

from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from src.schemas import user_info_response
from src.repositories import UserRepository
from src.helpers import CryptographyMessage


class AuthService:

    _user_repository = UserRepository()
    _security_field = CryptographyMessage()

    @classmethod
    def get_new_token(cls, _user_uuid: str) -> dict:
        user = cls._user_repository.get_user_by_uuid(_user_uuid)

        if not user:
            return {}

        try:
            credentials = cls._new_credentials(user, None)

            if not credentials.get('authorize', None):
                return {}

            credentials.pop('authorize')

            return credentials
        except Exception as e:
            logging.error(f'Error get new token: {e}')

    @classmethod
    def authorize(cls, _data: dict) -> dict:

        if len(_data) == 0:
            return {}

        try:
            email_encrypt = cls._security_field.encrypt(_data.get('email'))
            user = cls._user_repository.get_user_by_email(email_encrypt)

            if not user:
                return {}

            credentials = cls._new_credentials(user, _data.get('password'))

            if not credentials.get('authorize', None):
                return {}

            credentials.pop('authorize')

            return credentials
        except Exception as e:
            logging.error(f'Error authorize: {e}')

    @classmethod
    def _new_credentials(cls, _user: dict, _password: str | None) -> dict:
        if _password and not cls._verify_password(_password, _user.password_hash):
            return {'authorize': False}

        if _password and _user.deleted_at:
            data = {
                'deleted_at': None,
                'updated_at': datetime.now()
                }

            cls._user_repository.update_user(_user.uuid, data)

        add_claims = {
            'email': _user.email
            }

        access_token = create_access_token(identity=_user.uuid, additional_claims=add_claims)
        refresh_token = create_refresh_token(identity=_user.uuid, additional_claims=add_claims)

        credentials = user_info_response.dump(cls._user_format(_user))

        credentials.update({
            'authorize': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': 10800,
            'token_type': 'Bearer'
            })

        return credentials

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

    @classmethod
    def remove_access_user(cls, _jti, _ttype):
        try:
            cls._user_repository.blacklist_jwt(_jti, _ttype)
        except Exception as e:
            logging.error(f'Error get new token: {e}')

            return False

        return True

    @staticmethod
    def _verify_password(_password: str, _hashed_password: str) -> bool:
        combined_password = _password + os.environ.get('SECRET_KEY')

        return bcrypt.checkpw(combined_password.encode('utf-8'), _hashed_password.encode('utf-8'))
