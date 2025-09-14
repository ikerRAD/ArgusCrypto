from app.application import Instruction
from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query_response import \
    GetAllTickersByExchangeIdQueryResponse
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class GetAllTickersByExchangeIdQuery(Instruction):
    def __init__(self, ticker_repository: TickerRepository):
        self.__ticker_repository = ticker_repository

    def execute(self, exchange_id: int) -> GetAllTickersByExchangeIdQueryResponse:
        return GetAllTickersByExchangeIdQueryResponse(
            tickers=self.__ticker_repository.get_all_or_fail_by_exchange_id(exchange_id)
        )
