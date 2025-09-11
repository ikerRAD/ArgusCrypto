from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from backend.app.db import BaseModel


class Symbol(BaseModel):
    __tablename__ = "symbols"

    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "Ticker", back_populates="symbol", cascade="all, delete-orphan"
    )
