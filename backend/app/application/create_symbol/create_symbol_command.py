from app.application import Instruction
from app.application.create_symbol.create_symbol_command_response import (
    CreateSymbolCommandResponse,
)
from app.domain.crypto.models.symbol import Symbol
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class CreateSymbolCommand(Instruction):
    def __init__(self, symbol_repository: SymbolRepository):
        self.__symbol_repository = symbol_repository

    def execute(self, symbol: Symbol) -> CreateSymbolCommandResponse:
        created_symbol = self.__symbol_repository.insert(symbol)

        return CreateSymbolCommandResponse(created_symbol=created_symbol)
