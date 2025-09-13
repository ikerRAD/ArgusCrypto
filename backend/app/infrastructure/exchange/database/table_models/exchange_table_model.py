from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db import BaseTableModel


class ExchangeTableModel(BaseTableModel):
    __tablename__ = "exchanges"

    name = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "TickerTableModel", back_populates="exchange", cascade="all, delete-orphan"
    )
