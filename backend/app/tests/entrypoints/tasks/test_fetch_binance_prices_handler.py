from unittest import TestCase
from unittest.mock import Mock, patch

from httpx import ConnectTimeout

from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.entrypoints.tasks.fetch_binance_prices_handler import FetchBinancePricesHandler


class TestFetchBinancePricesHandler(TestCase):
    def setUp(self) -> None:
        self.update_prices_from_remote_command = Mock(
            spec=UpdatePricesFromRemoteCommand
        )

        self.handler = FetchBinancePricesHandler(
            command=self.update_prices_from_remote_command
        )

    @patch("app.entrypoints.tasks.fetch_binance_prices_handler.task_logger")
    def test_handle(self, logger: Mock) -> None:
        self.handler.handle()

        self.update_prices_from_remote_command.execute.assert_called_once()
        logger.info.assert_called_once_with("Fetching Binance prices...")
        logger.error.assert_not_called()

    @patch("app.entrypoints.tasks.fetch_binance_prices_handler.task_logger")
    def test_handle_binance_not_found(self, logger: Mock) -> None:
        exchange_not_found_exception = ExchangeNotFoundException("name", "Binance")
        self.update_prices_from_remote_command.execute.side_effect = (
            exchange_not_found_exception
        )

        self.handler.handle()

        self.update_prices_from_remote_command.execute.assert_called_once()
        logger.info.assert_called_once_with("Fetching Binance prices...")
        logger.error.assert_called_once_with(
            f"Binance is not a registered exchange: {exchange_not_found_exception}"
        )

    @patch("app.entrypoints.tasks.fetch_binance_prices_handler.task_logger")
    def test_handle_timeout(self, logger: Mock) -> None:
        self.update_prices_from_remote_command.execute.side_effect = ConnectTimeout(
            "timed out"
        )

        self.handler.handle()

        self.update_prices_from_remote_command.execute.assert_called_once()
        logger.info.assert_called_once_with("Fetching Binance prices...")
        logger.error.assert_called_once_with(
            "The connection to Binance API has timed out"
        )

    @patch("app.entrypoints.tasks.fetch_binance_prices_handler.task_logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        error = Exception("Something broke")
        self.update_prices_from_remote_command.execute.side_effect = error

        self.handler.handle()

        self.update_prices_from_remote_command.execute.assert_called_once()
        logger.info.assert_called_once_with("Fetching Binance prices...")
        logger.error.assert_called_once_with(
            f"An unexpected error happened while fetching Binance prices: {error}"
        )
