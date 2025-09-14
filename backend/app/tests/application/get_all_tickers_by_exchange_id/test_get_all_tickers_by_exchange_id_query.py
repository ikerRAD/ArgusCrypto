from unittest import TestCase
from unittest.mock import Mock

from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query import (
    GetAllTickersByExchangeIdQuery,
)
from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query_response import (
    GetAllTickersByExchangeIdQueryResponse,
)
from app.domain.crypto.models.ticker import Ticker
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class TestGetAllTickersByExchangeIdQuery(TestCase):
    def setUp(self) -> None:
        self.ticker_repository = Mock(spec=TickerRepository)

        self.query = GetAllTickersByExchangeIdQuery(self.ticker_repository)

    def test_execute(self) -> None:
        tickers = [
            Ticker(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT"),
            Ticker(id=2, symbol_id=1, exchange_id=1, ticker="BTCEUR"),
        ]
        self.ticker_repository.get_all_or_fail_by_exchange_id.return_value = tickers

        result = self.query.execute(1)

        self.assertEqual(
            GetAllTickersByExchangeIdQueryResponse(tickers=tickers), result
        )
        self.ticker_repository.get_all_or_fail_by_exchange_id.assert_called_once_with(1)
