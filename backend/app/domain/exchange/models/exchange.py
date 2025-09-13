from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Exchange:
    name: str
    id: None | int = field(default=None)
    tickers: list[Ticker] = field(default_factory=list)
