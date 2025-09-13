from fastapi import HTTPException

from app.application.get_all_symbols.get_all_symbols_query import GetAllSymbolsQuery
from app.dependency_injection_factories.application.get_all_symbols.get_all_symbols_query_factory import (
    GetAllSymbolsQueryFactory,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema
from app.tasks import logger


class GetAllSymbolsHandler(RouteHandler):
    def __init__(self, query: None | GetAllSymbolsQuery = None):
        self.__query = query or GetAllSymbolsQueryFactory.create()

    def handle(self) -> list[SymbolSchema]:
        try:
            logger.info("Getting all symbols from database")
            response = self.__query.execute()

            return [
                SymbolSchema.from_domain(domain_symbol)
                for domain_symbol in response.symbols
            ]
        except Exception as e:
            logger.error(
                f"An unexpected error happened while retrieving all symbols: {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
