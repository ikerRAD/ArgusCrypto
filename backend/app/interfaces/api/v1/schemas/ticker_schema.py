from __future__ import annotations
from pydantic import BaseModel

from app.domain.crypto.models.ticker import Ticker


class TickerSchema(BaseModel):
    id: int
    symbol_id: int
    exchange_id: int
    ticker: str

    @staticmethod
    def from_domain(domain_ticker: Ticker) -> TickerSchema:
        return TickerSchema(
            id=domain_ticker.id,
            symbol_id=domain_ticker.symbol_id,
            exchange_id=domain_ticker.exchange_id,
            ticker=domain_ticker.ticker,
        )
