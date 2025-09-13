from dataclasses import dataclass, field


@dataclass
class Ticker:
    symbol_id: int
    exchange_id: int
    ticker: str
    id: None | int = field(default=None)
