import logging

from src.schemas.user_schema import create_user_response
from src.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    @classmethod
    def create(cls, data: dict) -> dict:
        try:
            return create_user_response.dump(UserRepository.add(data))
        except Exception as e:
            logging.error(f'Error en create_user: {e}')
