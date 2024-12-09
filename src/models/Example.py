import uuid

from src.models.custom_columns import UUIDType
from src.config import db


class Example(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.PrimaryKeyConstraint('uuid'),)

    uuid = db.Column(
        UUIDType,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4)

    def __repr__(self):
        return f'User({self.uuid})'
