from unittest import TestCase

from app.domain.crypto.models.symbol import Symbol
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema


class TestSymbolSchema(TestCase):
    def test_from_domain(self) -> None:
        result = SymbolSchema.from_domain(Symbol(id=1, name="test", symbol="TST"))

        self.assertEqual(result, SymbolSchema(id=1, name="test", symbol="TST"))
