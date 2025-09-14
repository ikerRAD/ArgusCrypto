from dataclasses import dataclass

from app.application import Response
from app.domain.exchange.models.exchange import Exchange


@dataclass
class GetExchangeByIdQueryResponse(Response):
    exchange: Exchange
