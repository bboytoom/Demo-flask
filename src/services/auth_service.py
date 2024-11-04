import os
import bcrypt
import logging

from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from src.schemas import authorize_user_response
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

            column_names = ['uuid', 'email', 'password_hash', 'name', 'last_name', 'birth_day']
            data_dict = dict(zip(column_names, user))

            data_dict['name'] = cls._security_field.decrypt(user.name)
            data_dict['last_name'] = cls._security_field.decrypt(user.last_name)

            if user.birth_day:
                birth_day_decrypt = cls._security_field.decrypt(user.birth_day)
                data_dict['birth_day'] = datetime.strptime(birth_day_decrypt, '%Y-%m-%d')

            user_object = cls._user_repository.create_object(data_dict)
            credentials = authorize_user_response.dump(user_object)

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
