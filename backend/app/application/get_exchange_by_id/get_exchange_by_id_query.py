from app.application import Instruction
from app.application.get_exchange_by_id.get_exchange_by_id_query_response import (
    GetExchangeByIdQueryResponse,
)
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class GetExchangeByIdQuery(Instruction):
    def __init__(self, exchange_repository: ExchangeRepository):
        self.__exchange_repository = exchange_repository

    def execute(self, exchange_id: int) -> GetExchangeByIdQueryResponse:
        return GetExchangeByIdQueryResponse(
            exchange=self.__exchange_repository.get_or_fail_by_id(exchange_id)
        )
