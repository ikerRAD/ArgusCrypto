from dataclasses import dataclass, field


@dataclass
class Symbol:
    name: str
    symbol: str
    id: None | int = field(default=None)
