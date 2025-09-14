from unittest import TestCase

from app.domain.exchange.models.exchange import Exchange
from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema


class TestExchangeSchema(TestCase):
    def test_from_domain(self) -> None:
        result = ExchangeSchema.from_domain(Exchange(id=1, name="test"))

        self.assertEqual(result, ExchangeSchema(id=1, name="test"))
