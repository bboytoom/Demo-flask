import logging

from datetime import datetime
from sqlalchemy.orm import Mapped, \
    mapped_column

from sqlalchemy.exc import NoResultFound, \
    IntegrityError, \
    DataError

from src.config.sqlalchemy_db import db


class UserStockSymbol(db.Model):
    __tablename__ = 'user_stock_symbol'
    __table_args__ = (
        db.PrimaryKeyConstraint('user_uuid', 'stock_symbol_uuid'),
        db.Index('ix_user_stock_symbol', 'user_uuid', 'stock_symbol_uuid'),
        db.UniqueConstraint('user_uuid', 'stock_symbol_uuid', name='uq_user_stock_symbol'),)

    user_uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        db.ForeignKey('users.uuid', ondelete='CASCADE'),
        primary_key=True,
        index=True,
        nullable=False)

    stock_symbol_uuid = mapped_column(
        db.CHAR(36),
        db.ForeignKey('stock_symbol.uuid', ondelete='CASCADE'),
        primary_key=True,
        index=True,
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)

    def __repr__(self):
        return f'UserStockSymbol({self.user_uuid}, {self.stock_symbol_uuid})'

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
