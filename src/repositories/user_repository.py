import logging

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound, DataError, IntegrityError

from src.config import db, jwt_blacklist, ACCESS_EXPIRES
from src.models import User


class UserRepository:

    def get_user_by_email(self, _email: str) -> User:
        try:
            query = (
                db.session.query(
                    User.uuid,
                    User.email,
                    User.password_hash,
                    User.name,
                    User.last_name,
                    User.birth_day,
                    User.created_at,
                    User.updated_at,
                    User.deleted_at
                    ).filter(and_(User.email == _email, User.status)))

            return query.first()
        except NoResultFound:
            logging.error('User does not exist')

            raise TypeError('User does not exist')
        except Exception as e:
            logging.error(f'Search User error: {e}')

            raise

    def create_object(self, _data: dict) -> User:
        return User(uuid=_data.get('uuid', None),
                    email=_data.get('email'),
                    password_hash=_data.get('password'),
                    name=_data.get('name'),
                    last_name=_data.get('last_name'),
                    birth_day=_data.get('birth_day', None),
                    status=_data.get('status', True),
                    created_at=_data.get('created_at'),
                    updated_at=_data.get('updated_at'))

    def add(self, _data: dict) -> User:
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

    def update_user(self, _user_uuid: str, _data: dict) -> User:
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        try:
            db.session.query(User).filter_by(uuid=_user_uuid).update(_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error update user info: {e}')

            raise

        return self.create_object(_data)

    def remove_user(self, _user_uuid: str, _data) -> None:
        try:
            db.session.query(User).filter_by(uuid=_user_uuid).update(_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error remove user info: {e}')

            raise

        return None

    def blacklist_jwt(self, _jti, _ttype):
        try:
            jwt_blacklist.set(_jti, _ttype,  ex=ACCESS_EXPIRES)
        except Exception as e:
            logging.error(f'Error remove web token: {e}')

            raise

        return True
