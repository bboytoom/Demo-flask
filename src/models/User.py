import enum
import logging

from datetime import datetime
from src.config.sqlalchemy_db import db


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
        nullable=False
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

    @classmethod
    def new_user(cls, _data):
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
        db.session.add(self)
        db.session.commit()
