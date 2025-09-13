from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import Result
from sqlalchemy.orm import Session

from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models.exchange import Exchange
from app.infrastructure.exchange.database.repositories.db_exchange_repository import (
    DbExchangeRepository,
)


class TestDbBinanceRepository(TestCase):
    def setUp(self) -> None:
        self.exchange = Exchange(name="Binance")

        self.repository = DbExchangeRepository()

    @patch(
        "app.infrastructure.exchange.repositories.db_exchange_repository.get_session"
    )
    def test_find_exchange(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = self.exchange
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        result = self.repository.find_exchange("Binance", False)

        self.assertEqual(result, self.exchange)
        self.assertEqual(result.tickers, [])

        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.repositories.db_exchange_repository.get_session"
    )
    def test_find_exchange_fetching_tickers(self, get_session: Mock) -> None:
        tickers = [
            Ticker(symbol_id=1, exchange_id=1, ticker="SOME"),
            Ticker(symbol_id=2, exchange_id=1, ticker="OTHER"),
            Ticker(symbol_id=3, exchange_id=1, ticker="TICKER"),
            Ticker(symbol_id=4, exchange_id=1, ticker="HERE"),
        ]
        self.exchange.tickers = tickers
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = self.exchange
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        result = self.repository.find_exchange("Binance", True)

        self.assertEqual(result, self.exchange)
        self.assertEqual(result.tickers, tickers)

        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.repositories.db_exchange_repository.get_session"
    )
    def test_find_exchange_not_found(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = None
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        with self.assertRaisesRegex(
            ExchangeNotFoundException, "exchange with name 'Some' not found'"
        ):
            self.repository.find_exchange("Some", False)

        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()
