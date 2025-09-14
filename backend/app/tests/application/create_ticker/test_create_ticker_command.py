from unittest import TestCase
from unittest.mock import Mock

from app.application.create_ticker.create_ticker_command import CreateTickerCommand
from app.application.create_ticker.create_ticker_command_response import (
    CreateTickerCommandResponse,
)
from app.domain.crypto.models.ticker import Ticker
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class TestCreateTickerCommand(TestCase):
    def setUp(self) -> None:
        self.ticker_repository = Mock(spec=TickerRepository)

        self.command = CreateTickerCommand(self.ticker_repository)

    def test_execute(self) -> None:
        ticker = Ticker(ticker="ETHEUR", symbol_id=1, exchange_id=1)
        created_ticker = Ticker(id=1, ticker="ETHEUR", symbol_id=1, exchange_id=1)
        self.ticker_repository.insert.return_value = created_ticker

        result = self.command.execute(ticker)

        self.assertEqual(
            CreateTickerCommandResponse(created_ticker=created_ticker), result
        )
        self.ticker_repository.insert.assert_called_once_with(ticker)
