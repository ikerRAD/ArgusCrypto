from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Ticker:
    symbol_id: int
    exchange_id: int
    ticker: str
    id: None | int = field(default=None)
    prices: list[Price] = field(default_factory=list)
    symbol: None | Symbol = field(default=None)
    exchange: None | Exchange = field(default=None)
