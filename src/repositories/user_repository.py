import logging

from src.models.user import User
from src.config.sqlalchemy_db import db

from sqlalchemy.exc import NoResultFound, DataError, IntegrityError


class UserRepository:

    @classmethod
    def get_by_uuid(cls, _uuid: str) -> User:
        try:
            query = (db.session.query(User).filter(User.uuid == _uuid))

            return query.first()
        except NoResultFound:
            logging.error('User does not exist')

            raise TypeError('User does not exist')
        except Exception as e:
            logging.error(f'Search User error: {e}')

            raise

    @classmethod
    def add(cls, _data: dict) -> User:
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        user = User(name=_data.get('name'),
                    last_name=_data.get('last_name'),
                    birth_day=_data.get('birth_day'),
                    status=_data.get('status', True))

        return cls._save(user)

    @staticmethod
    def _save(_data: User) -> User:
        try:
            db.session.add(_data)
            db.session.commit()

            return _data
        except IntegrityError:
            db.session.rollback()
            logging.error('Duplicated data')

            raise TypeError('Duplicated data in database')
        except DataError:
            db.session.rollback()
            logging.error('Error was inserted data ')

            raise TypeError('Data error was inserted')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error inserting data: {e}')

            raise
