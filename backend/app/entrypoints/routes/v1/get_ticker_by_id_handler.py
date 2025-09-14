from fastapi import HTTPException

from app.application.get_ticker_by_id.get_ticker_by_id_query import GetTickerByIdQuery
from app.dependency_injection_factories.application.get_ticker_by_id.get_ticker_by_id_query_factory import (
    GetTickerByIdQueryFactory,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema
from app.main import logger


class GetTickerByIdHandler(RouteHandler):
    def __init__(self, query: None | GetTickerByIdQuery = None):
        self.__query = query or GetTickerByIdQueryFactory.create()

    def handle(self, ticker_id) -> TickerSchema:
        try:
            logger.info(f"Retrieving ticker with id '{ticker_id}'")
            response = self.__query.execute(ticker_id)

            return TickerSchema.from_domain(response.ticker)
        except TickerNotFoundException:
            logger.error(f"Ticker with id '{ticker_id}' not found")
            raise HTTPException(status_code=404, detail="Ticker not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving ticker with id '{ticker_id}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
