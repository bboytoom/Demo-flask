import uuid
import logging

from datetime import datetime

from src.config.sqlalchemy_db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import NoResultFound, IntegrityError, DataError


class HistoricalStockPrice(db.Model):
    __tablename__ = 'historical_stock_price'
    __table_args__ = (
        db.PrimaryKeyConstraint('uuid'),
        db.Index('ix_stock_symbol_date_stock', 'stock_symbol_uuid', 'date_stock'),)

    uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4)

    stock_symbol_uuid: Mapped[str] = mapped_column(
        db.CHAR(36),
        db.ForeignKey('stock_symbol.uuid', ondelete='CASCADE'),
        index=True,
        nullable=False)

    open_price = db.Column(db.Float(4, 3), default=0.0)
    high_price = db.Column(db.Float(4, 3), default=0.0)
    low_price = db.Column(db.Float(4, 3), default=0.0)
    close_price = db.Column(db.Float(4, 3), default=0.0)

    date_stock = db.Column(
        db.Date,
        index=True,
        nullable=False)

    time_stock = db.Column(
        db.Time,
        nullable=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)

    def __repr__(self):
        return f'HistoricalStockPrice({self.uuid}, {self.stock_symbol_uuid})'

    @classmethod
    def new_historical_stock_price(cls, _data):
        if len(_data) == 0:
            raise NoResultFound('The model is empty.')

        return HistoricalStockPrice(
            stock_symbol_uuid=_data.get('stock_symbol_uuid'),
            open_price=_data.get('open_price'),
            high_price=_data.get('high_price'),
            low_price=_data.get('low_price'),
            close_price=_data.get('close_price'),
            date_stock=_data.get('date_stock'),
            time_stock=_data.get('time_stock')
            )

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
