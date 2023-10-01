import enum
import uuid

from datetime import datetime
from src.config.sqlalchemy_db import db


class TypeOnboarding(enum.Enum):
    ONBOARDING_STEP_ONE = 'ONBOARDING_STEP_ONE'
    ONBOARDING_STEP_TWO = 'ONBOARDING_STEP_TWO'


class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
        )

    name = db.Column(db.String(25), nullable=False)
    web_identifier = db.Column(db.String(36), nullable=False)

    onboarding = db.Column(
        db.Enum(TypeOnboarding),
        nullable=False
        )

    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
        default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        )

    def __repr__(self):
        return f'User({self.uuid}, {self.name}, {self.onboarding})'
