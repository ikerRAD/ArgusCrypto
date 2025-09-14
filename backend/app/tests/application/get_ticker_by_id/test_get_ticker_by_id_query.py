from unittest import TestCase
from unittest.mock import Mock

from app.application.get_ticker_by_id.get_ticker_by_id_query import GetTickerByIdQuery
from app.application.get_ticker_by_id.get_ticker_by_id_query_response import GetTickerByIdQueryResponse
from app.domain.crypto.models.ticker import Ticker
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class TestGetTickerByIdQuery(TestCase):
    def setUp(self) -> None:
        self.ticker_repository = Mock(spec=TickerRepository)

        self.query = GetTickerByIdQuery(self.ticker_repository)

    def test_execute(self):
        ticker = Ticker(id=1,symbol_id=1,exchange_id=1,ticker="BTCUSDT")
        self.ticker_repository.get_or_fail_by_id.return_value = ticker

        result = self.query.execute(1)

        self.assertEqual(GetTickerByIdQueryResponse(ticker=ticker),result)
        self.ticker_repository.get_or_fail_by_id.assert_called_once_with(ticker.id)
