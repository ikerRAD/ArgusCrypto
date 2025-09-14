from unittest import TestCase
from unittest.mock import Mock

from app.application.get_all_exchanges.get_all_exchanges_query import (
    GetAllExchangesQuery,
)
from app.application.get_all_exchanges.get_all_exchanges_query_response import (
    GetAllExchangesQueryResponse,
)
from app.domain.exchange.models.exchange import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class TestGetAllExchangesQuery(TestCase):
    def setUp(self) -> None:
        self.exchange_repository = Mock(spec=ExchangeRepository)

        self.query = GetAllExchangesQuery(self.exchange_repository)

    def test_execute(self) -> None:
        exchanges = [Exchange(id=1, name="Binance"), Exchange(id=2, name="Kraken")]
        self.exchange_repository.get_all.return_value = exchanges

        result = self.query.execute()

        self.assertEqual(result, GetAllExchangesQueryResponse(exchanges=exchanges))
        self.exchange_repository.get_all.assert_called_once()
