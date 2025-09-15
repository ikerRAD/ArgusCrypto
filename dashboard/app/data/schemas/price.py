from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Price:
    id: int
    ticker_id: int
    price: float
    timestamp: datetime
