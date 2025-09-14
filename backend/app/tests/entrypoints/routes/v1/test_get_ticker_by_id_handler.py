from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_ticker_by_id.get_ticker_by_id_query import GetTickerByIdQuery
from app.application.get_ticker_by_id.get_ticker_by_id_query_response import GetTickerByIdQueryResponse
from app.domain.crypto.exceptions.ticker_not_found_exception import TickerNotFoundException
from app.domain.crypto.models.ticker import Ticker
from app.entrypoints.routes.v1.get_ticker_by_id_handler import GetTickerByIdHandler
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema


class TestGetTickerByIdHandler(TestCase):
    def setUp(self) -> None:
        self.get_ticker_by_id_query = Mock(spec=GetTickerByIdQuery)

        self.handler = GetTickerByIdHandler(self.get_ticker_by_id_query)

    @patch("app.entrypoints.routes.v1.get_ticker_by_id_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        query_response = GetTickerByIdQueryResponse(
            ticker=Ticker(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT")
        )
        self.get_ticker_by_id_query.execute.return_value = query_response

        result = self.handler.handle(1)

        self.assertEqual(TickerSchema(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT"), result)
        logger.info.assert_called_once_with("Retrieving ticker with id '1'")
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_ticker_by_id_handler.logger")
    def test_handle_not_found(self, logger: Mock) -> None:
        self.get_ticker_by_id_query.execute.side_effect = TickerNotFoundException(12)

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(12)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(context.exception.detail, "Ticker not found")
            logger.error.assert_called_once_with("Ticker with id '12' not found")

        logger.info.assert_called_once_with("Retrieving ticker with id '12'")

    @patch("app.entrypoints.routes.v1.get_ticker_by_id_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_ticker_by_id_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(1)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"Unexpected error occurred while retrieving ticker with id '1': {context.exception}"
            )

        logger.info.assert_called_once_with("Retrieving ticker with id '1'")
