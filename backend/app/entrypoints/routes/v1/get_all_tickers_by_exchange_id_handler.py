from fastapi import HTTPException

from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query import \
    GetAllTickersByExchangeIdQuery
from app.dependency_injection_factories.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query_factory import \
    GetAllTickersByExchangeIdQueryFactory
from app.domain.exchange.exceptions.exchange_not_found_exception import ExchangeNotFoundException
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema
from app.main import logger


class GetAllTickersByExchangeIdHandler(RouteHandler):
    def __init__(self, query: None | GetAllTickersByExchangeIdQuery = None):
        self.__query = query or GetAllTickersByExchangeIdQueryFactory.create()

    def handle(self, exchange_id: int) -> list[TickerSchema]:
        try:
            logger.info(f"Getting all tickers for exchange '{exchange_id}' from database")
            response = self.__query.execute(exchange_id)

            return [TickerSchema.from_domain(ticker) for ticker in response.tickers]
        except ExchangeNotFoundException:
            logger.error(f"Exchange with id '{exchange_id}' not found")
            raise HTTPException(status_code=404, detail="Exchange not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving tickers for exchange with id '{exchange_id}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")