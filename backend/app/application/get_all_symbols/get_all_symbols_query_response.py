from dataclasses import dataclass

from app.application import Response
from app.domain.crypto.models.symbol import Symbol


@dataclass(frozen=True)
class GetAllSymbolsQueryResponse(Response):
    symbols: list[Symbol]
