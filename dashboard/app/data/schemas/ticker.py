from dataclasses import dataclass


@dataclass(frozen=True)
class Ticker:
    id: int
    symbol_id: int
    exchange_id: int
    ticker: str
