from unittest import TestCase
from unittest.mock import Mock

from app.domain.exchange.models.exchange import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository
from app.infrastructure.exchange.finders.binance_exchange_finder import (
    BinanceExchangeFinder,
)


class TestBinanceExchangeFinder(TestCase):
    def setUp(self) -> None:
        self.exchange = Exchange(name="Binance")
        self.exchange_repository = Mock(spec=ExchangeRepository)
        self.exchange_repository.find_exchange.return_value = self.exchange

        self.finder = BinanceExchangeFinder(self.exchange_repository)

    def test_find(self) -> None:
        result = self.finder.find()

        self.assertEqual(result, self.exchange)
        self.exchange_repository.find_exchange.assert_called_once_with("Binance", False)

    def test_find_fetch_tickers(self) -> None:
        result = self.finder.find(fetch_tickers=True)

        self.assertEqual(result, self.exchange)
        self.exchange_repository.find_exchange.assert_called_once_with("Binance", True)
