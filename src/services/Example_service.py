import logging

from src.schemas import example_response
from src.repositories import ExampleRepository
from src.helpers import CryptographyMessage


class ExampleService:

    _user_repository = ExampleRepository()
    _security_field = CryptographyMessage()

    @classmethod
    def retrieve(cls, _user_uuid: str) -> dict:
        user = cls._user_repository.get_user_by_uuid(_user_uuid)

        return example_response.dump(user)

    @classmethod
    def create(cls, _data: dict) -> dict:
        try:
            insert_data = cls._user_repository.add(_data)
        except Exception as e:
            if e.args[0] == 'Duplicated data in database':
                return {
                    'code': 409
                    }

            logging.error(f'Error create_user: {e}')

        return example_response.dump(insert_data)
