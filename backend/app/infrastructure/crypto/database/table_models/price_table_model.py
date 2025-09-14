from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Index
from sqlalchemy.orm import relationship

from app.db import Base


class PriceTableModel(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker_id = Column(
        Integer, ForeignKey("tickers.id", ondelete="cascade"), nullable=False
    )
    price = Column(Float, nullable=False)
    timestamp = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    ticker = relationship("TickerTableModel", back_populates="prices")

    __table_args__ = (
        Index("prices_index_ticker_id_timestamp", "ticker_id", "timestamp"),
    )
