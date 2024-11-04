import uuid

from datetime import datetime

from src.config import db


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

    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birth_day = db.Column(db.String(255), nullable=True)
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
        return f'User({self.uuid}, {self.email}, {self.name}, {self.last_name}, {self.birth_day})'
