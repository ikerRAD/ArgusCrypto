from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship

from app.db import Base


class TickerTableModel(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol_id = Column(
        Integer, ForeignKey("symbols.id", ondelete="cascade"), nullable=False
    )
    exchange_id = Column(
        Integer, ForeignKey("exchanges.id", ondelete="cascade"), nullable=False
    )
    ticker = Column(String, nullable=False)

    prices = relationship(
        "PriceTableModel", back_populates="ticker", cascade="all, delete-orphan"
    )

    symbol = relationship("SymbolTableModel", back_populates="tickers")
    exchange = relationship("ExchangeTableModel", back_populates="tickers")

    __table_args__ = (
        UniqueConstraint("exchange_id", "ticker", name="unique_exchange_ticker"),
    )
