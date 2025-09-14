from unittest import TestCase
from unittest.mock import Mock

from app.application.get_exchange_by_id.get_exchange_by_id_query import (
    GetExchangeByIdQuery,
)
from app.application.get_exchange_by_id.get_exchange_by_id_query_response import (
    GetExchangeByIdQueryResponse,
)
from app.domain.exchange.models.exchange import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class TestGetExchangeByIdQuery(TestCase):
    def setUp(self) -> None:
        self.exchange_repository = Mock(spec=ExchangeRepository)

        self.query = GetExchangeByIdQuery(self.exchange_repository)

    def test_execute(self) -> None:
        exchange = Exchange(id=1, name="Binane")
        self.exchange_repository.get_or_fail_by_id.return_value = exchange

        result = self.query.execute(1)

        self.assertEqual(GetExchangeByIdQueryResponse(exchange=exchange), result)
        self.exchange_repository.get_or_fail_by_id.assert_called_with(1)
