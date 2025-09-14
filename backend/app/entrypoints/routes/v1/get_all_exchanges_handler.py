from fastapi import HTTPException

from app.application.get_all_exchanges.get_all_exchanges_query import (
    GetAllExchangesQuery,
)
from app.dependency_injection_factories.application.get_all_exchanges.get_all_exchanges_query_factory import (
    GetAllExchangesQueryFactory,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema
from app.main import logger


class GetAllExchangesHandler(RouteHandler):
    def __init__(self, query: None | GetAllExchangesQuery = None):
        self.__query = query or GetAllExchangesQueryFactory.create()

    def handle(self) -> list[ExchangeSchema]:
        try:
            logger.info("Getting all exchanges from database")
            response = self.__query.execute()

            return [
                ExchangeSchema.from_domain(exchange) for exchange in response.exchanges
            ]
        except Exception as e:
            logger.error(
                f"An unexpected error happened while querying all exchanges: {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
