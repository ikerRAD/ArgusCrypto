from dataclasses import dataclass, field

from app.domain.crypto.models.ticker import Ticker


@dataclass
class Exchange:
    name: str
    id: None | int = field(default=None)
    tickers: None | list[Ticker] = field(default=None)
