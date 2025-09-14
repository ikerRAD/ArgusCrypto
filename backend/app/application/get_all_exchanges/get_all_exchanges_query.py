from app.application import Instruction
from app.application.get_all_exchanges.get_all_exchanges_query_response import (
    GetAllExchangesQueryResponse,
)
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class GetAllExchangesQuery(Instruction):
    def __init__(self, exchange_repository: ExchangeRepository):
        self.__exchange_repository = exchange_repository

    def execute(self) -> GetAllExchangesQueryResponse:
        return GetAllExchangesQueryResponse(
            exchanges=self.__exchange_repository.get_all()
        )
