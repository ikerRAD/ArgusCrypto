from unittest import TestCase
from unittest.mock import Mock

from app.application.get_all_symbols.get_all_symbols_query import GetAllSymbolsQuery
from app.application.get_all_symbols.get_all_symbols_query_response import GetAllSymbolsQueryResponse
from app.domain.crypto.models.symbol import Symbol
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class TestGetAllSymbolsQuery(TestCase):
    def setUp(self) -> None:
        self.symbol_repository = Mock(spec=SymbolRepository)

        self.query = GetAllSymbolsQuery(self.symbol_repository)

    def test_execute(self) -> None:
        symbols = [
            Symbol(name="test", symbol="TST"),
            Symbol(name="test2", symbol="T2T")
        ]
        self.symbol_repository.get_all.return_value = symbols

        result = self.query.execute()

        self.assertEqual(result, GetAllSymbolsQueryResponse(symbols=symbols))
        self.symbol_repository.get_all.assert_called_once()