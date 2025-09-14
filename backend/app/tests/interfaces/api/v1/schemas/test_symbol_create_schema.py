from unittest import TestCase

from app.domain.crypto.models.symbol import Symbol
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema


class TestSymbolCreateSchema(TestCase):
    def test_to_domain(self) -> None:
        result = SymbolCreateSchema.to_domain(
            SymbolCreateSchema(name="test", symbol="TST")
        )

        self.assertEqual(result, Symbol(name="test", symbol="TST"))
