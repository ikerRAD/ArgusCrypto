from dataclasses import dataclass

from app.application import Response
from app.domain.exchange.models.exchange import Exchange


@dataclass(frozen=True)
class GetAllExchangesQueryResponse(Response):
    exchanges: list[Exchange]
