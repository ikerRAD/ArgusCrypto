from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Index, func
from sqlalchemy.orm import relationship

from app.db import BaseModel


class DbPrice(BaseModel):
    __tablename__ = "prices"

    ticker_id = Column(
        Integer, ForeignKey("tickers.id", ondelete="cascade"), nullable=False
    )
    price = Column(Float, nullable=False)
    timestamp = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    ticker = relationship("Ticker", back_populates="prices")

    __table_args__ = (
        Index("prices_index_ticker_id_timestamp", "ticker_id", "timestamp"),
    )
