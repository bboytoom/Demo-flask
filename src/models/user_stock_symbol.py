import uuid
import logging

from datetime import datetime
from sqlalchemy.orm import Mapped, \
    mapped_column, \
    relationship, \
    validates

from sqlalchemy.exc import NoResultFound, \
    IntegrityError, \
    DataError

from src.config.sqlalchemy_db import db


class UserStockSymbol(db.Model):
    __tablename__ = 'user_stock_symbol'
    __table_args__ = (
        db.Index('ix_user_stock_symbol', 'user_uuid', 'stock_symbol_uuid'),
        db.UniqueConstraint('user_uuid', 'stock_symbol_uuid', name='uq_user_stock_symbol'))

    uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4)

    user_uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        db.ForeignKey('users.uuid', ondelete='CASCADE'),
        index=True,
        nullable=False)

    stock_symbol_uuid = mapped_column(
        db.CHAR(36),
        db.ForeignKey('stock_symbol.uuid', ondelete='CASCADE'),
        index=True,
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)

    def __repr__(self):
        return f'UserStockSymbol({self.uuid}, {self.user_uuid}, {self.stock_symbol_uuid})'

    @validates('user_uuid', 'stock_symbol_uuid')
    def validate_name(self, _key: str, _value: str):
        if not _value:
            raise ValueError('The name is empty')

        return _value

    @classmethod
    def new_user(cls, _data: dict):
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        return UserStockSymbol(
            user_uuid=_data.get('user_uuid'),
            stock_symbol_uuid=_data.get('stock_symbol_uuid'))

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
