import uuid
import logging

from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, \
    mapped_column, \
    relationship, \
    validates

from sqlalchemy.exc import NoResultFound, \
    IntegrityError, \
    DataError

from src.config.sqlalchemy_db import db
from src.models.user_stock_symbol import UserStockSymbol


class StockSymbol(db.Model):
    __tablename__ = 'stock_symbol'

    uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4)

    symbol_name = db.Column(
        db.String(50),
        nullable=True)

    symbol = db.Column(
        db.String(20),
        index=True,
        nullable=False)

    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)

    _user_stock_symbol: Mapped[List[UserStockSymbol]] = relationship(
        cascade="all, delete",
        passive_deletes=True)

    def __repr__(self):
        return f'StockSymbol({self.uuid}, {self.symbol})'

    @validates('symbol')
    def validate_last_name(self, _key: str, _value: str):
        if not _value:
            raise ValueError('The symbol is empty')

        if len(_value) <= 3 or len(_value) >= 20:
            raise ValueError('The symbol must be between 3 to 20 characters')

        return _value

    @classmethod
    def new_stock_symbol(cls, _data: dict):
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        return StockSymbol(
            symbol_name=_data.get('symbol_name'),
            symbol=_data.get('symbol'),
            status=_data.get('status'))

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
