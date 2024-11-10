import os
import bcrypt
import logging

from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from src.schemas import user_response, authorize_user_response
from src.repositories import UserRepository
from src.helpers import CryptographyMessage


class AuthService:

    _user_repository = UserRepository()
    _security_field = CryptographyMessage()

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
            if _password:
                email_encrypt = cls._security_field.encrypt(_email)
            else:
                email_encrypt = _email

            user = cls._user_repository.get_user_by_email(email_encrypt)

            if _password and not cls._verify_password(_password, user.password_hash):
                return {'authorize': False}

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            credentials = authorize_user_response.dump(cls._user_format(user))

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

    @classmethod
    def verify_the_same_token_user(cls, _email: str, _user_uuid: str) -> dict:
        user = cls._user_repository.get_user_by_email(_email)

        if not (user.uuid == _user_uuid):
            return None

        return user_response.dump(cls._user_format(user))

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
    def _verify_password(_password: str, _hashed_password: str) -> bool:
        combined_password = _password + os.environ.get('SECRET_KEY')

        return bcrypt.checkpw(combined_password.encode('utf-8'), _hashed_password.encode('utf-8'))
