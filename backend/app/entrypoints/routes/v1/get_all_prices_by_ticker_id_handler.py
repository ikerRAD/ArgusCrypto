from datetime import datetime

from fastapi import HTTPException

from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query import (
    GetAllPricesByTickerIdQuery,
)
from app.dependency_injection_factories.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query_factory import (
    GetAllPricesByTickerIdQueryFactory,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.price_schema import PriceSchema
from app.main import logger


class GetAllPricesByTickerIdHandler(RouteHandler):
    def __init__(self, query: None | GetAllPricesByTickerIdQuery = None):
        self.__query = query or GetAllPricesByTickerIdQueryFactory.create()

    def handle(
        self, ticker_id: int, start_date: None | datetime, end_date: None | datetime
    ) -> list[PriceSchema]:
        if start_date is not None and end_date is not None and start_date > end_date:
            logger.error(
                f"Invalid date range [{start_date}, {end_date}] for querying prices for ticker '{ticker_id}'"
            )
            raise HTTPException(
                status_code=400, detail="start_date must be before end_date"
            )

        try:
            logger.info(
                f"Getting prices for ticker '{ticker_id}' in date range [{start_date}, {end_date}]"
            )
            response = self.__query.execute(ticker_id, start_date, end_date)

            return [PriceSchema.from_domain(price) for price in response.prices]
        except TickerNotFoundException:
            logger.error(f"Ticker with id '{ticker_id}' not found")
            raise HTTPException(status_code=404, detail="Ticker not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving prices for ticker with id '{ticker_id}' in date range [{start_date}, {end_date}]: {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
