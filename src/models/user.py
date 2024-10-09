import uuid
import logging

from datetime import datetime

from src.config.sqlalchemy_db import db

from sqlalchemy.orm import validates
from sqlalchemy.exc import NoResultFound, IntegrityError, DataError


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.PrimaryKeyConstraint('uuid'),)
    # db.Index('ix_user_stock_symbol', 'user_uuid', 'stock_symbol_uuid'),
    # db.UniqueConstraint('user_uuid', 'stock_symbol_uuid', name='uq_user_stock_symbol'),

    uuid = db.Column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4)

    name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    birth_day = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.now,
        default=datetime.now)

    def __repr__(self):
        return f'User({self.uuid}, {self.name}, {self.last_name})'

    @validates('name')
    def validate_name(self, _key: str, _value: str):
        if not _value:
            raise ValueError('The name is empty')

        if len(_value) <= 2 or len(_value) >= 30:
            raise ValueError('The name must be between 2 to 30 characters')

        return _value

    @validates('last_name')
    def validate_last_name(self, _key: str, _value: str):
        if not _value:
            raise ValueError('The last_name is empty')

        if len(_value) <= 2 or len(_value) >= 70:
            raise ValueError('The last_name must be between 2 to 70 characters')

        return _value

    @classmethod
    def new_user(cls, _data: dict):
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        return User(
            name=_data.get('name'),
            last_name=_data.get('last_name'),
            birth_day=_data.get('birth_day'),
            status=_data.get('status'))

    def search_user(_user_uuid):
        try:
            return db.session.query(User) \
                .filter(User.uuid == str(_user_uuid)).first()
        except Exception as e:
            logging.error(f'Search User error: {e}')

            raise TypeError(f'Error in search user {e}')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except IntegrityError as err:
            logging.error(f'Duplicated data : {err}')

            raise TypeError('Duplicated data in database')
        except DataError as err:
            logging.error(f'Error was inserted data : {err}')

            db.session.rollback()

            raise TypeError('Data error was inserted')
