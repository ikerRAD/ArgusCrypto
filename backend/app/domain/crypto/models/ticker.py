from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship

from backend.app.db import BaseModel


class Ticker(BaseModel):
    __tablename__ = "tickers"

    symbol_id = Column(
        Integer, ForeignKey("symbols.id", ondelete="cascade"), nullable=False
    )
    exchange_id = Column(
        Integer, ForeignKey("exchanges.id", ondelete="cascade"), nullable=False
    )
    ticker = Column(String, nullable=False)

    prices = relationship(
        "Price", back_populates="ticker", cascade="all, delete-orphan"
    )

    symbol = relationship("Symbol", back_populates="tickers")
    exchange = relationship("Exchange", back_populates="tickers")

    __table_args__ = (
        UniqueConstraint("exchange_id", "ticker", name="unique_exchange_ticker"),
    )
