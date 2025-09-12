from unittest import TestCase
from unittest.mock import Mock

from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.domain.crypto.models import Ticker, Price
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.domain.exchange.clients.exchange_client import ExchangeClient
from app.domain.exchange.finders.exchange_finder import ExchangeFinder
from app.domain.exchange.models import Exchange


class TestUpdatePricesFromRemoteCommand(TestCase):
    def setUp(self) -> None:
        self.exchange_client = Mock(spec=ExchangeClient)
        self.exchange_finder = Mock(spec=ExchangeFinder)
        self.price_repository = Mock(spec=PriceRepository)

        self.command = UpdatePricesFromRemoteCommand(
            self.exchange_client, self.exchange_finder, self.price_repository
        )

    def test_execute(self) -> None:
        tickers = [Ticker(), Ticker()]
        self.exchange_finder.find.return_value = Exchange(tickers=tickers)

        fetched_prices = [Price(), Price()]
        self.exchange_client.fetch_price_for_tickers.return_value = fetched_prices

        self.command.execute()

        self.exchange_finder.find.assert_called_once_with(fetch_tickers=True)
        self.exchange_client.fetch_price_for_tickers.assert_called_once_with(tickers)
        self.price_repository.bulk_save.assert_called_once_with(fetched_prices)
