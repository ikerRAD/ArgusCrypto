from app.application import Instruction
from app.application.get_all_symbols.get_all_symbols_query_response import (
    GetAllSymbolsQueryResponse,
)
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class GetAllSymbolsQuery(Instruction):
    def __init__(self, symbol_repository: SymbolRepository):
        self.__symbol_repository = symbol_repository

    def execute(self) -> GetAllSymbolsQueryResponse:
        return GetAllSymbolsQueryResponse(symbols=self.__symbol_repository.get_all())
