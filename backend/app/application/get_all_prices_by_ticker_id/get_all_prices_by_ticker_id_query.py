from datetime import datetime

from app.application import Instruction
from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query_response import (
    GetAllPricesByTickerIdQueryResponse,
)
from app.domain.crypto.repositories.price_repository import PriceRepository


class GetAllPricesByTickerIdQuery(Instruction):
    def __init__(self, price_repository: PriceRepository):
        self.__price_repository = price_repository

    def execute(
        self,
        ticker_id: int,
        start_date: None | datetime,
        end_date: None | datetime,
        include_end=True,
        check_ticker=True,
    ) -> GetAllPricesByTickerIdQueryResponse:
        return GetAllPricesByTickerIdQueryResponse(
            prices=self.__price_repository.get_all_or_fail_by_ticker_id(
                ticker_id, start_date, end_date, include_end, check_ticker
            )
        )
