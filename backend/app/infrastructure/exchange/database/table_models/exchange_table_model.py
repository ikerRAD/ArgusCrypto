from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class ExchangeTableModel(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "TickerTableModel", back_populates="exchange", cascade="all, delete-orphan"
    )
