from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db import BaseTableModel


class SymbolTableModel(BaseTableModel):
    __tablename__ = "symbols"

    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "TickerTableModel", back_populates="symbol", cascade="all, delete-orphan"
    )
