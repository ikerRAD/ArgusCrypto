from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.create_ticker.create_ticker_command import CreateTickerCommand
from app.application.create_ticker.create_ticker_command_response import (
    CreateTickerCommandResponse,
)
from app.domain.crypto.exceptions.reference_to_non_existent_id_exception import (
    ReferenceToNonExistentIdException,
)
from app.domain.crypto.exceptions.ticker_already_exists_exception import (
    TickerAlreadyExistsException,
)
from app.domain.crypto.models.ticker import Ticker
from app.entrypoints.routes.v1.post_ticker_handler import PostTickerHandler
from app.interfaces.api.v1.schemas.ticker_create_schema import TickerCreateSchema
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema


class TestPostTickerHandler(TestCase):
    def setUp(self) -> None:
        self.create_ticker_command = Mock(spec=CreateTickerCommand)

        self.handler = PostTickerHandler(self.create_ticker_command)

    @patch("app.entrypoints.routes.v1.post_ticker_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        command_response = CreateTickerCommandResponse(
            created_ticker=Ticker(id=1, ticker="BTCUSDT", exchange_id=1, symbol_id=1)
        )
        self.create_ticker_command.execute.return_value = command_response
        ticker_create = TickerCreateSchema(ticker="BTCUSDT", exchange_id=1, symbol_id=1)

        result = self.handler.handle(ticker_create)

        self.assertEqual(
            result, TickerSchema(id=1, ticker="BTCUSDT", exchange_id=1, symbol_id=1)
        )
        self.create_ticker_command.execute.assert_called_once_with(
            Ticker(ticker="BTCUSDT", exchange_id=1, symbol_id=1)
        )
        logger.info.assert_called_once_with(
            "Creating ticker 'BTCUSDT' for exchange '1' and symbol '1'"
        )
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.post_ticker_handler.logger")
    def test_handle_symbol_exists(self, logger: Mock) -> None:
        self.create_ticker_command.execute.side_effect = TickerAlreadyExistsException(
            "BTCUSDT", 1
        )
        ticker_create = TickerCreateSchema(ticker="BTCUSDT", exchange_id=1, symbol_id=1)

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(ticker_create)

            self.assertEqual(context.exception.status_code, 409)
            self.assertEqual(
                context.exception.detail,
                "Ticker 'BTCUSDT' already exists for exchange '1'",
            )
            logger.error.assert_called_once_with(
                "Ticker 'BTCUSDT' already exists for exchange '1'"
            )

        self.create_ticker_command.execute.assert_called_once_with(
            Ticker(ticker="BTCUSDT", exchange_id=1, symbol_id=1)
        )
        logger.info.assert_called_once_with(
            "Creating ticker 'BTCUSDT' for exchange '1' and symbol '1'"
        )

    @patch("app.entrypoints.routes.v1.post_ticker_handler.logger")
    def test_handle_symbol_exchange_id_not_exists(self, logger: Mock) -> None:
        self.create_ticker_command.execute.side_effect = (
            ReferenceToNonExistentIdException("exchange_id", 15)
        )
        ticker_create = TickerCreateSchema(
            ticker="BTCUSDT", exchange_id=15, symbol_id=1
        )

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(ticker_create)

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(
                context.exception.detail, "exchange_id '15' is non-existent"
            )
            logger.error.assert_called_once_with(
                f"symbol_id '15' or exchange_id '1' are non-existent: {context.exception}"
            )

        self.create_ticker_command.execute.assert_called_once_with(
            Ticker(ticker="BTCUSDT", exchange_id=15, symbol_id=1)
        )
        logger.info.assert_called_once_with(
            "Creating ticker 'BTCUSDT' for exchange '15' and symbol '1'"
        )

    @patch("app.entrypoints.routes.v1.post_ticker_handler.logger")
    def test_handle_symbol_symbol_id_not_exists(self, logger: Mock) -> None:
        self.create_ticker_command.execute.side_effect = (
            ReferenceToNonExistentIdException("symbol_id", 15)
        )
        ticker_create = TickerCreateSchema(
            ticker="BTCUSDT", exchange_id=1, symbol_id=15
        )

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(ticker_create)

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "symbol_id '15' is non-existent")
            logger.error.assert_called_once_with(
                f"symbol_id '1' or exchange_id '15' are non-existent: {context.exception}"
            )

        self.create_ticker_command.execute.assert_called_once_with(
            Ticker(ticker="BTCUSDT", exchange_id=1, symbol_id=15)
        )
        logger.info.assert_called_once_with(
            "Creating ticker 'BTCUSDT' for exchange '1' and symbol '15'"
        )

    @patch("app.entrypoints.routes.v1.post_ticker_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.create_ticker_command.execute.side_effect = Exception()
        ticker_create = TickerCreateSchema(ticker="BTCUSDT", exchange_id=1, symbol_id=1)

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(ticker_create)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"An unexpected error happened creating the ticker 'BTCUSDT' "
                f"for exchange '1' and symbol '1': {context.exception}"
            )

        self.create_ticker_command.execute.assert_called_once_with(
            Ticker(ticker="BTCUSDT", exchange_id=1, symbol_id=1)
        )
        logger.info.assert_called_once_with(
            "Creating ticker 'BTCUSDT' for exchange '1' and symbol '1'"
        )
