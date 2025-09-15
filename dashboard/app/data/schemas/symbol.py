from dataclasses import dataclass


@dataclass(frozen=True)
class Symbol:
    id: int
    name: str
    symbol: str
