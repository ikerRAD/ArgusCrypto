from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel

from app.domain.crypto.models.price import Price


class PriceSchema(BaseModel):
    id: int
    ticker_id: int
    price: float
    timestamp: datetime

    @staticmethod
    def from_domain(domain_price: Price) -> PriceSchema:
        return PriceSchema(
            id=domain_price.id,
            ticker_id=domain_price.ticker_id,
            price=domain_price.price,
            timestamp=domain_price.timestamp,
        )
