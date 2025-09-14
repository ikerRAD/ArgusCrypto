from dataclasses import dataclass

from app.application import Response
from app.domain.crypto.models.ticker import Ticker


@dataclass(frozen=True)
class GetAllTickersByExchangeIdQueryResponse(Response):
    tickers: list[Ticker]
