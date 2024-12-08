from datetime import datetime

from src.repositories import UserRepository
from src.helpers import CryptographyMessage


_user_repository = UserRepository()
_security_field = CryptographyMessage()


def user_format(_data):
    column_names = ['uuid', 'email', 'password_hash', 'name', 'last_name', 'birth_day',
                    'created_at', 'updated_at']

    data_dict = dict(zip(column_names, _data))

    data_dict['email'] = _security_field.decrypt(_data.email)
    data_dict['name'] = _security_field.decrypt(_data.name)
    data_dict['last_name'] = _security_field.decrypt(_data.last_name)

    if _data.birth_day:
        birth_day_decrypt = _security_field.decrypt(_data.birth_day)
        data_dict['birth_day'] = datetime.strptime(birth_day_decrypt, '%Y-%m-%d')

    return _user_repository.create_object(data_dict)
