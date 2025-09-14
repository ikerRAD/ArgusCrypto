from unittest import TestCase
from unittest.mock import Mock

from app.application.get_symbol_by_id.get_symbol_by_id_query import GetSymbolByIdQuery
from app.application.get_symbol_by_id.get_symbol_by_id_query_response import (
    GetSymbolByIdQueryResponse,
)
from app.domain.crypto.models.symbol import Symbol
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class TestGetSymbolByIdQuery(TestCase):
    def setUp(self) -> None:
        self.symbol_repository = Mock(spec=SymbolRepository)

        self.query = GetSymbolByIdQuery(self.symbol_repository)

    def test_execute(self) -> None:
        symbol = Symbol(id=1, name="test", symbol="TST")
        self.symbol_repository.get_or_fail_by_id.return_value = symbol
        expected_response = GetSymbolByIdQueryResponse(symbol=symbol)

        result = self.query.execute(1)

        self.assertEqual(expected_response, result)
        self.symbol_repository.get_or_fail_by_id.assert_called_once_with(symbol.id)
