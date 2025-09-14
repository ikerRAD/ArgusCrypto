from datetime import datetime
from unittest import TestCase

from app.domain.crypto.models.price import Price
from app.interfaces.api.v1.schemas.price_schema import PriceSchema


class TestPriceSchema(TestCase):
    def test_from_domain(self) -> None:
        result = PriceSchema.from_domain(
            Price(id=1, price=2.0, ticker_id=1, timestamp=datetime(2020, 3, 3))
        )

        self.assertEqual(
            result,
            PriceSchema(id=1, price=2.0, ticker_id=1, timestamp=datetime(2020, 3, 3)),
        )
