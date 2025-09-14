from __future__ import annotations
from pydantic import BaseModel

from app.domain.crypto.models.ticker import Ticker


class TickerCreateSchema(BaseModel):
    id: int
    symbol_id: int
    exchange_id: int
    ticker: str

    @staticmethod
    def to_domain(ticker_create_schema: TickerCreateSchema) -> Ticker:
        return Ticker(
            id=ticker_create_schema.id,
            symbol_id=ticker_create_schema.symbol_id,
            exchange_id=ticker_create_schema.exchange_id,
            ticker=ticker_create_schema.ticker,
        )
