from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class SymbolTableModel(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "TickerTableModel", back_populates="symbol", cascade="all, delete-orphan"
    )
