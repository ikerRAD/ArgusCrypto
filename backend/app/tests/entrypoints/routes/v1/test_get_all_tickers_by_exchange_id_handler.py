from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query import \
    GetAllTickersByExchangeIdQuery
from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query_response import \
    GetAllTickersByExchangeIdQueryResponse
from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.exceptions.exchange_not_found_exception import ExchangeNotFoundException
from app.entrypoints.routes.v1.get_all_tickers_by_exchange_id_handler import GetAllTickersByExchangeIdHandler
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema


class TestGetAllTickersByExchangeIdHandler(TestCase):
    def setUp(self) -> None:
        self.get_all_tickers_by_exchange_id_query = Mock(spec=GetAllTickersByExchangeIdQuery)

        self.handler = GetAllTickersByExchangeIdHandler(self.get_all_tickers_by_exchange_id_query)

    @patch("app.entrypoints.routes.v1.get_all_tickers_by_exchange_id_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        tickers = [
            Ticker(
                id=1,
                symbol_id=1,
                exchange_id=1,
                ticker="BTCUSDT"
            ),
            Ticker(
                id=2,
                symbol_id=1,
                exchange_id=1,
                ticker="BTCEUR"
            )
        ]
        query_response = GetAllTickersByExchangeIdQueryResponse(
            tickers=tickers
        )
        self.get_all_tickers_by_exchange_id_query.execute.return_value = query_response

        result = self.handler.handle(1)

        self.assertEqual([TickerSchema(
                id=1,
                symbol_id=1,
                exchange_id=1,
                ticker="BTCUSDT"
            ),TickerSchema(
                id=2,
                symbol_id=1,
                exchange_id=1,
                ticker="BTCEUR"
            )], result)
        logger.info.assert_called_once_with(
            "Getting all tickers for exchange '1' from database"
        )
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_tickers_by_exchange_id_handler.logger")
    def test_handle_not_found(self, logger: Mock) -> None:
        self.get_all_tickers_by_exchange_id_query.execute.side_effect = ExchangeNotFoundException(
            "id", 12
        )

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(12)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(context.exception.detail, "Exchange not found")
            logger.error.assert_called_once_with("Exchange with id '12' not found")

        logger.info.assert_called_once_with(
            "Getting all tickers for exchange '12' from database"
        )

    @patch("app.entrypoints.routes.v1.get_all_tickers_by_exchange_id_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_all_tickers_by_exchange_id_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(1)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"Unexpected error occurred while retrieving tickers for exchange with id '1': {context.exception}"
            )

        logger.info.assert_called_once_with(
            "Getting all tickers for exchange '1' from database"
        )
