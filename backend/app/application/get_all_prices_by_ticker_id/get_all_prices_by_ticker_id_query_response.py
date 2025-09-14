from dataclasses import dataclass

from app.application import Response
from app.domain.crypto.models.price import Price


@dataclass(frozen=True)
class GetAllPricesByTickerIdQueryResponse(Response):
    prices: list[Price]
