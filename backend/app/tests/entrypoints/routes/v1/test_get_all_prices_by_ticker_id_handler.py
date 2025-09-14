from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query import (
    GetAllPricesByTickerIdQuery,
)
from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query_response import (
    GetAllPricesByTickerIdQueryResponse,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.price import Price
from app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler import (
    GetAllPricesByTickerIdHandler,
)
from app.interfaces.api.v1.schemas.price_schema import PriceSchema


class TestGetAllPricesByTickerIdHandler(TestCase):
    def setUp(self) -> None:
        self.get_all_prices_by_ticker_id_query = Mock(spec=GetAllPricesByTickerIdQuery)
        self.start_date = datetime(2013, 1, 1)
        self.end_date = datetime(2015, 1, 1)

        self.handler = GetAllPricesByTickerIdHandler(
            self.get_all_prices_by_ticker_id_query, 0.001
        )

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        prices = [
            Price(id=1, price=2.0, ticker_id=1, timestamp=datetime(2013, 1, 1)),
            Price(id=2, price=20.0, ticker_id=1, timestamp=datetime(2014, 1, 1)),
            Price(id=3, price=200.0, ticker_id=1, timestamp=datetime(2015, 1, 1)),
        ]
        self.get_all_prices_by_ticker_id_query.execute.return_value = (
            GetAllPricesByTickerIdQueryResponse(prices=prices)
        )

        result = self.handler.handle(1, self.start_date, self.end_date)

        self.assertEqual(
            result,
            [
                PriceSchema(
                    id=1, price=2.0, ticker_id=1, timestamp=datetime(2013, 1, 1)
                ),
                PriceSchema(
                    id=2, price=20.0, ticker_id=1, timestamp=datetime(2014, 1, 1)
                ),
                PriceSchema(
                    id=3, price=200.0, ticker_id=1, timestamp=datetime(2015, 1, 1)
                ),
            ],
        )
        self.get_all_prices_by_ticker_id_query.execute.assert_called_once_with(
            1, self.start_date, self.end_date
        )
        logger.info.assert_called_once_with(
            f"Getting prices for ticker '1' in date range [{self.start_date}, {self.end_date}]"
        )
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    def test_handle_invalid_range(self, logger: Mock) -> None:
        with self.assertRaises(HTTPException) as context:
            self.handler.handle(1, self.end_date, self.start_date)

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(
                context.exception.detail, "start_date must be before end_date"
            )
            logger.error.assert_called_once_with(
                f"Invalid date range [{self.end_date}, {self.start_date}] for querying prices for ticker '1'"
            )

        self.get_all_prices_by_ticker_id_query.execute.assert_not_called()
        logger.info.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    def test_handle_ticker_not_found(self, logger: Mock) -> None:
        self.get_all_prices_by_ticker_id_query.execute.side_effect = (
            TickerNotFoundException(100)
        )

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(100, self.start_date, self.end_date)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(context.exception.detail, "Ticker not found")
            logger.error.assert_called_once_with("Ticker with id '100' not found")

        self.get_all_prices_by_ticker_id_query.execute.assert_called_once()
        logger.info.assert_called_once_with(
            f"Getting prices for ticker '100' in date range [{self.start_date}, {self.end_date}]"
        )

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_all_prices_by_ticker_id_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(1, self.start_date, self.end_date)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"Unexpected error occurred while retrieving prices for ticker with id '1' in date range [{self.start_date}, {self.end_date}]: {e}"
            )

        self.get_all_prices_by_ticker_id_query.execute.assert_called_once()
        logger.info.assert_called_once_with(
            f"Getting prices for ticker '1' in date range [{self.start_date}, {self.end_date}]"
        )

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    async def test_handle_websocket(self, logger: Mock) -> None:
        prices = [
            Price(id=1, price=2.0, ticker_id=1, timestamp=datetime(2013, 1, 1)),
            Price(id=2, price=20.0, ticker_id=1, timestamp=datetime(2014, 1, 1)),
            Price(id=3, price=200.0, ticker_id=1, timestamp=datetime(2015, 1, 1)),
        ]
        self.get_all_prices_by_ticker_id_query.execute.return_value = (
            GetAllPricesByTickerIdQueryResponse(prices=prices)
        )
        websocket = Mock(spec=WebSocket)
        websocket.send_json.side_effect = [None, None, WebSocketDisconnect()]

        try:
            await self.handler.handle_websocket(websocket, 1, 100)
        except WebSocketDisconnect:

            self.assertEqual(3, self.get_all_prices_by_ticker_id_query.execute.call_count)
            logger.info.assert_not_called()
            logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    async def test_handle_websocket_ticker_not_found(self, logger: Mock) -> None:
        self.get_all_prices_by_ticker_id_query.execute.side_effect = TickerNotFoundException(1)
        websocket = Mock(spec=WebSocket)

        try:
            await self.handler.handle_websocket(websocket, 1, 100)
        except TickerNotFoundException:

            self.get_all_prices_by_ticker_id_query.execute.assert_called_once()
            logger.info.assert_not_called()
            logger.error.assert_called_once_with("Ticker with id '1' not found")
            websocket.send_json.assert_called_once_with({"error": "Ticker not found"})

    @patch("app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler.logger")
    async def test_handle_websocket_unexpected_error(self, logger: Mock) -> None:
        self.get_all_prices_by_ticker_id_query.execute.side_effect = Exception()
        websocket = Mock(spec=WebSocket)

        try:
            await self.handler.handle_websocket(websocket, 1, 100)
        except Exception as e:

            self.get_all_prices_by_ticker_id_query.execute.assert_called_once()
            logger.info.assert_not_called()
            logger.error.assert_called_once_with(f"An unexpected error happened in price websocket: {e}")
            websocket.send_json.assert_called_once_with({"error": "An unexpected error happened"})
