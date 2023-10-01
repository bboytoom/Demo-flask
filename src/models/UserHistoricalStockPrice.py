import uuid

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
        default=uuid.uuid4
        )

    user_uuid = db.Column(
        db.CHAR(36),
        db.ForeignKey('users.uuid'),
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
        default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
        default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        )

    def __repr__(self):
        return f'UserHistoricalStockPrice({self.uuid}, {self.user_uuid}, {self.symbol_stock})'
