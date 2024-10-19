import uuid

from datetime import datetime
from src.config.sqlalchemy_db import db

from sqlalchemy.orm import validates


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.PrimaryKeyConstraint('uuid'),)

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
