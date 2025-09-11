from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db import BaseModel


class Exchange(BaseModel):
    __tablename__ = "exchanges"

    name = Column(String, nullable=False, unique=True)

    tickers = relationship(
        "Ticker", back_populates="exchange", cascade="all, delete-orphan"
    )
