from unittest import TestCase

from app.domain.crypto.models.ticker import Ticker
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema


class TestTickerSchema(TestCase):
    def test_from_domain(self):
        result = TickerSchema.from_domain(
            Ticker(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT")
        )

        self.assertEqual(
            result, TickerSchema(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT")
        )
