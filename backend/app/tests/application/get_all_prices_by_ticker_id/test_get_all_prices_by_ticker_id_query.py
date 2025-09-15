from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query import (
    GetAllPricesByTickerIdQuery,
)
from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query_response import (
    GetAllPricesByTickerIdQueryResponse,
)
from app.domain.crypto.models.price import Price
from app.domain.crypto.repositories.price_repository import PriceRepository


class TestGetAllPricesByTickerIdQuery(TestCase):
    def setUp(self) -> None:
        self.price_repository = Mock(spec=PriceRepository)

        self.query = GetAllPricesByTickerIdQuery(self.price_repository)

    def test_execute(self):
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2020, 1, 1)
        price = Price(id=1, price=2.0, ticker_id=1, timestamp=datetime(2013, 1, 1))
        self.price_repository.get_all_or_fail_by_ticker_id.return_value = [price]

        response = self.query.execute(1, start_date=start_date, end_date=end_date)

        self.assertEqual(GetAllPricesByTickerIdQueryResponse(prices=[price]), response)
        self.price_repository.get_all_or_fail_by_ticker_id.assert_called_with(
            1, start_date, end_date, True, True
        )
