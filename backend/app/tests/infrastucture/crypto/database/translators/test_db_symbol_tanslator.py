from unittest import TestCase

from app.domain.crypto.models.symbol import Symbol
from app.infrastructure.crypto.database.table_models import SymbolTableModel
from app.infrastructure.crypto.database.translators.db_symbol_translator import DbSymbolTranslator


class TestDbSymbolTranslator(TestCase):
    def setUp(self) -> None:
        self.translator = DbSymbolTranslator()

    def test_translate_to_domain_model(self) -> None:
        result = self.translator.translate_to_domain_model(SymbolTableModel(id=1,name="Bitcoin",symbol="BTC"))

        self.assertEqual(result,Symbol(id=1,name="Bitcoin",symbol="BTC"))

    def test_bulk_translate_to_domain_model(self) -> None:
        result = self.translator.bulk_translate_to_domain_model([
            SymbolTableModel(id=1,name="Bitcoin",symbol="BTC"),
            SymbolTableModel(id=2,name="Ethereum",symbol="ETH")
        ])

        self.assertEqual(result,[Symbol(id=1,name="Bitcoin",symbol="BTC"), Symbol(id=2,name="Ethereum",symbol="ETH")])