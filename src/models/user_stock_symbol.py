from datetime import datetime

from src.config.sqlalchemy_db import db
from sqlalchemy.orm import Mapped, mapped_column


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

    stock_symbol_uuid: Mapped[str] = mapped_column(
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
