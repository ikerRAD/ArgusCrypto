from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_all_exchanges.get_all_exchanges_query import GetAllExchangesQuery
from app.application.get_all_exchanges.get_all_exchanges_query_response import GetAllExchangesQueryResponse
from app.domain.exchange.models.exchange import Exchange
from app.entrypoints.routes.v1.get_all_exchanges_handler import GetAllExchangesHandler
from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema


class TestGetAllExchangesHandler(TestCase):
    def setUp(self) -> None:
        self.get_all_exchanges_query = Mock(spec=GetAllExchangesQuery)

        self.handler = GetAllExchangesHandler(self.get_all_exchanges_query)

    @patch("app.entrypoints.routes.v1.get_all_exchanges_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        exchanges = [Exchange(id=1, name="Binance"),Exchange(id=2, name="Kraken")]
        self.get_all_exchanges_query.execute.return_value = GetAllExchangesQueryResponse(exchanges=exchanges)

        result = self.handler.handle()

        self.assertEqual(result, [ExchangeSchema(id=1, name="Binance"), ExchangeSchema(id=2, name="Kraken")])
        self.get_all_exchanges_query.execute.assert_called_once()
        logger.info.assert_called_once_with("Getting all exchanges from database")
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_exchanges_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_all_exchanges_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle()

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"An unexpected error happened while querying all exchanges: {context.exception}"
            )

        self.get_all_exchanges_query.execute.assert_called_once()
        logger.info.assert_called_once_with("Getting all exchanges from database")
