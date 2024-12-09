import logging

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound, DataError, IntegrityError

from src.config import db
from src.models import Example


class ExampleRepository:

    def get_user_by_uuid(value: str) -> Example:
        try:
            query = (
                db.session.query(Example.uuid,).filter(and_(Example.uuid == value)))

            return query.first()
        except NoResultFound:
            logging.error('User does not exist')

            raise TypeError('User does not exist')
        except Exception as e:
            logging.error(f'Search User error: {e}')

            raise

    def create_object(self, _data: dict) -> Example:
        return Example(uuid=_data.get('uuid', None))

    def add(self, _data: dict) -> Example:
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        try:
            db.session.add(self.create_object(_data))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning('Duplicated data')

            raise TypeError('Duplicated data in database')
        except DataError:
            db.session.rollback()
            logging.error('Error was inserted data ')

            raise TypeError('Data error was inserted')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error inserting data: {e}')

            raise

        return _data
