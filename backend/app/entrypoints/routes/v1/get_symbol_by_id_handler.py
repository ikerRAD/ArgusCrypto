from fastapi import HTTPException

from app.application.get_symbol_by_id.get_symbol_by_id_query import GetSymbolByIdQuery
from app.dependency_injection_factories.application.get_symbol_by_id.get_symbol_by_id_query_factory import (
    GetSymbolByIdQueryFactory,
)
from app.domain.crypto.exceptions.symbol_not_found_exception import (
    SymbolNotFoundException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema
from app.main import logger


class GetSymbolByIdHandler(RouteHandler):
    def __init__(self, query: None | GetSymbolByIdQuery = None):
        self.__query = query or GetSymbolByIdQueryFactory.create()

    def handle(self, symbol_id: int) -> SymbolSchema:
        try:
            logger.info(f"Getting symbol with id '{symbol_id}' from database")
            response = self.__query.execute(symbol_id)

            return SymbolSchema.from_domain(response.symbol)
        except SymbolNotFoundException:
            logger.error(f"Symbol with id '{symbol_id}' not found")
            raise HTTPException(status_code=404, detail="Symbol not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving symbol with id '{symbol_id}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
