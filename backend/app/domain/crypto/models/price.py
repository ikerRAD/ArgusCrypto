from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Price:
    ticker_id: int
    price: float
    id: None | int = field(default=None)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
