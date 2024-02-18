import uuid
import logging

from sqlalchemy import and_
from datetime import datetime, date, time
from src.config.sqlalchemy_db import db


class UserHistoricalStockPrice(db.Model):
    __tablename__ = 'users_historical_stock_price'
    """__table_args__ = (
        db.Index('ix_web_identifier_symbol', 'web_identifier_uuid', 'symbol_stock'),
        )"""

    uuid = db.Column(
        db.CHAR(36),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
        )

    web_identifier_uuid = db.Column(
        db.CHAR(36),
        # db.ForeignKey('users.web_identifier'),
        index=True,
        nullable=False
        )

    symbol_stock = db.Column(
        db.String(20),
        index=True,
        nullable=False)

    open_price = db.Column(db.Float(4, 3), default=0.0)
    high_price = db.Column(db.Float(4, 3), default=0.0)
    low_price = db.Column(db.Float(4, 3), default=0.0)
    close_price = db.Column(db.Float(4, 3), default=0.0)

    date_stock = db.Column(db.Date, nullable=False)

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
            date_stock=date.fromisoformat(_data.get('date_stock')),
            time_stock=time.fromisoformat(_data.get('time_stock'))
            )

    def search_history_price(_web_identifier: str, _symbol: str = None):
        try:
            if not _symbol:
                clause = UserHistoricalStockPrice.web_identifier_uuid == _web_identifier
            else:
                clause = and_(UserHistoricalStockPrice.web_identifier_uuid == _web_identifier,
                              UserHistoricalStockPrice.symbol_stock == _symbol)

            return db.session.query(UserHistoricalStockPrice).filter(clause)
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
