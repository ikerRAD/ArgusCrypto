from unittest import TestCase
from unittest.mock import Mock, patch

from sqlalchemy import Result
from sqlalchemy.orm import Session

from app.domain.crypto.models.symbol import Symbol
from app.infrastructure.crypto.database.repositories.db_symbol_repository import DbSymbolRepository
from app.infrastructure.crypto.database.table_models import SymbolTableModel
from app.infrastructure.crypto.database.translators.db_symbol_translator import DbSymbolTranslator


class TestDbSymbolRepository(TestCase):
    def setUp(self) -> None:
        self.db_symbol_translator = Mock(spec=DbSymbolTranslator)

        self.repository = DbSymbolRepository(self.db_symbol_translator)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_symbol_repository.get_session"
    )
    def test_get_all(self, get_session: Mock) -> None:
        symbol_table_models = [
            SymbolTableModel(id=1,name="Bitcoin",symbol="BTC"),
            SymbolTableModel(id=2,name="Ethereum",symbol="ETH")
        ]
        query_result = Mock(spec=Result)
        query_result.scalars.return_value.all.return_value = symbol_table_models
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        session.execute.return_value = query_result
        symbols = [
            Symbol(id=1,name="Bitcoin",symbol="BTC"),
            Symbol(id=2,name="Ethereum",symbol="ETH")
        ]
        self.db_symbol_translator.bulk_translate_to_domain_model.return_value = symbols


        result = self.repository.get_all()

        self.assertEqual(symbols, result)
        self.db_symbol_translator.bulk_translate_to_domain_model.assert_called_once_with(symbol_table_models)
        query_result.scalars.assert_called_once()
        query_result.scalars.return_value.all.assert_called_once()
        session.execute.assert_called_once()
