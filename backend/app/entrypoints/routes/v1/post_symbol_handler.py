from fastapi import HTTPException

from app.application.create_symbol.create_symbol_command import CreateSymbolCommand
from app.dependency_injection_factories.application.create_symbol.create_symbol_command_factory import (
    CreateSymbolCommandFactory,
)
from app.domain.crypto.exceptions.symbol_already_exists_exception import (
    SymbolAlreadyExistsException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema
from app.main import logger


class PostSymbolHandler(RouteHandler):
    def __init__(self, command: None | CreateSymbolCommand = None):
        self.__command = command or CreateSymbolCommandFactory.create()

    def handle(self, symbol_schema: SymbolCreateSchema) -> SymbolSchema:
        try:
            logger.info(f"Creating symbol '{symbol_schema.symbol}'")
            response = self.__command.execute(
                SymbolCreateSchema.to_domain(symbol_schema)
            )

            return SymbolSchema.from_domain(response.created_symbol)
        except SymbolAlreadyExistsException:
            logger.error(f"Symbol '{symbol_schema.symbol}' already exists")
            raise HTTPException(
                status_code=409,
                detail=f"Symbol '{symbol_schema.symbol}' already exists",
            )
        except Exception as e:
            logger.error(
                f"An unexpected error happened creating the symbol '{symbol_schema.symbol}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
