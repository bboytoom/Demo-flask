import enum
import logging

from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.exc import NoResultFound, \
    IntegrityError, \
    DataError

from src.config.sqlalchemy_db import db
from src.helpers.validations_for_functions import validate_uuid


class TypeOnboarding(enum.Enum):
    ONBOARDING_STEP_ONE = 'ONBOARDING_STEP_ONE'
    ONBOARDING_STEP_TWO = 'ONBOARDING_STEP_TWO'


class User(db.Model):
    __tablename__ = 'users'

    web_identifier = db.Column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False)

    name = db.Column(db.String(25), nullable=False)

    onboarding = db.Column(
        db.Enum(TypeOnboarding),
        nullable=False,
        default=TypeOnboarding.ONBOARDING_STEP_ONE.value,
        )

    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
        )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.now,
        default=datetime.now
        )

    def __repr__(self):
        return f'User({self.web_identifier}, {self.name}, {self.onboarding})'

    @validates('web_identifier')
    def validate_web_identifier(self, key: str, _value: str):
        if not _value:
            raise ValueError('The web_identifier is empty')

        if not validate_uuid(_value):
            raise ValueError('The web_identifier does not uuid')

        return _value

    @validates('name')
    def validate_name(self, _key: str, _value: str):
        if not _value:
            raise ValueError('The name is empty')

        if len(_value) <= 2 or len(_value) >= 25:
            raise ValueError('The name must be between 2 to 25 characters')

        return _value

    @classmethod
    def new_user(cls, _data: dict):
        if len(_data) == 0:
            raise NoResultFound('The model is empty')

        return User(
            name=_data.get('name'),
            web_identifier=_data.get('web_identifier'),
            onboarding=_data.get('onboarding'),
            status=_data.get('status')
            )

    def retrieve_user(_web_identifier: str):
        try:
            return db.session.query(User.web_identifier, User.name, User.onboarding) \
                .filter(User.web_identifier == _web_identifier).first_or_404()
        except Exception as e:
            logging.error(f'Search User error: {e}')

            raise

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
