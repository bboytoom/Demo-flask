import uuid
import logging

from sqlalchemy import and_
from datetime import datetime
from src.config.sqlalchemy_db import db


class UserHistoricalStockPrice(db.Model):
    __tablename__ = 'users_historical_stock_price'

    uuid = db.Column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=str(uuid.uuid4())
        )

    web_identifier_uuid = db.Column(
        db.CHAR(36),
        db.ForeignKey('users.web_identifier'),
        index=True,
        nullable=False
        )

    symbol_stock = db.Column(db.String(20), nullable=False)

    open_price = db.Column(db.Float(4, 3), default=1)
    high_price = db.Column(db.Float(4, 3), default=1)
    low_price = db.Column(db.Float(4, 3), default=1)
    close_price = db.Column(db.Float(4, 3), default=1)

    date_stock = db.Column(db.Date, index=True, nullable=False)

    time_stock = db.Column(
        db.Time,
        nullable=True
        )

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
        return f'UserHistoricalStockPrice({self.web_identifier_uuid}, {self.symbol_stock})'

    @classmethod
    def new_price(cls, _data):
        return UserHistoricalStockPrice(
            web_identifier_uuid=_data.get('web_identifier_uuid'),
            symbol_stock=_data.get('symbol_stock'),
            open_price=_data.get('open_price'),
            high_price=_data.get('high_price'),
            low_price=_data.get('low_price'),
            close_price=_data.get('close_price'),
            date_stock=_data.get('date_stock'),
            time_stock=_data.get('time_stock')
            )

    def search_history_price(_web_identifier, _symbol):
        try:
            return db.session.query(UserHistoricalStockPrice) \
                .filter(and_(UserHistoricalStockPrice.web_identifier_uuid == _web_identifier,
                             UserHistoricalStockPrice.symbol_stock == _symbol)).all()
        except Exception as e:
            logging.error(f'Search User History error: {e}')

            raise

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return True
        except Exception as e:
            logging.error(f'Insert User History error: {e}')

            return False
