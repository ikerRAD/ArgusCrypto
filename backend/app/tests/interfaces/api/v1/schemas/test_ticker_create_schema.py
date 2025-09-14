from unittest import TestCase

from app.domain.crypto.models.ticker import Ticker
from app.interfaces.api.v1.schemas.ticker_create_schema import TickerCreateSchema


class TestTickerCreateSchema(TestCase):
    def test_to_domain(self) -> None:
        result = TickerCreateSchema.to_domain(
            TickerCreateSchema(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT")
        )

        self.assertEqual(
            result, Ticker(id=1, symbol_id=1, exchange_id=1, ticker="BTCUSDT")
        )
