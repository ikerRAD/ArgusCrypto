from app.application import Instruction
from app.application.get_ticker_by_id.get_ticker_by_id_query_response import (
    GetTickerByIdQueryResponse,
)
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class GetTickerByIdQuery(Instruction):
    def __init__(self, ticker_repository: TickerRepository):
        self.__ticker_repository = ticker_repository

    def execute(self, ticker_id: int) -> GetTickerByIdQueryResponse:
        return GetTickerByIdQueryResponse(
            ticker=self.__ticker_repository.get_or_fail_by_id(ticker_id)
        )
