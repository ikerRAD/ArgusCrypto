from app.application import Instruction
from app.application.get_symbol_by_id.get_symbol_by_id_query_response import (
    GetSymbolByIdQueryResponse,
)
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class GetSymbolByIdQuery(Instruction):
    def __init__(self, symbol_repository: SymbolRepository):
        self.__symbol_repository = symbol_repository

    def execute(self, symbol_id: int) -> GetSymbolByIdQueryResponse:
        return GetSymbolByIdQueryResponse(
            symbol=self.__symbol_repository.get_or_fail_by_id(symbol_id)
        )
