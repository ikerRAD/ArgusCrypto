from app.application import Instruction
from app.application.create_symbol.create_symbol_command_response import (
    CreateSymbolCommandResponse,
)
from app.domain.crypto.repositories.symbol_repository import SymbolRepository
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema


class CreateSymbolCommand(Instruction):
    def __init__(self, symbol_repository: SymbolRepository):
        self.__symbol_repository = symbol_repository

    def execute(self, symbol_schema: SymbolCreateSchema) -> CreateSymbolCommandResponse:
        created_symbol = self.__symbol_repository.insert(
            SymbolCreateSchema.to_domain(symbol_schema)
        )

        return CreateSymbolCommandResponse(created_symbol=created_symbol)
