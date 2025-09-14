from fastapi import HTTPException

from app.application.get_exchange_by_id.get_exchange_by_id_query import (
    GetExchangeByIdQuery,
)
from app.dependency_injection_factories.application.get_exchange_by_id.get_exchange_by_id_query_factory import (
    GetExchangeByIdQueryFactory,
)
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema
from app.main import logger


class GetExchangeByIdHandler(RouteHandler):
    def __init__(self, query: None | GetExchangeByIdQuery = None):
        self.__query = query or GetExchangeByIdQueryFactory.create()

    def handle(self, exchange_id: int) -> ExchangeSchema:
        try:
            logger.info(f"Getting exchange with id '{exchange_id}' from database")
            response = self.__query.execute(exchange_id)

            return ExchangeSchema.from_domain(response.exchange)
        except ExchangeNotFoundException:
            logger.error(f"Exchange with id '{exchange_id}' not found")
            raise HTTPException(status_code=404, detail="Exchange not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving exchange with id '{exchange_id}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
