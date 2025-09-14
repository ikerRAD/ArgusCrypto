from unittest import TestCase
from unittest.mock import Mock

from app.application.create_symbol.create_symbol_command import CreateSymbolCommand
from app.application.create_symbol.create_symbol_command_response import (
    CreateSymbolCommandResponse,
)
from app.domain.crypto.models.symbol import Symbol
from app.domain.crypto.repositories.symbol_repository import SymbolRepository


class TestCreateSymbolCommand(TestCase):
    def setUp(self) -> None:
        self.symbol_repository = Mock(spec=SymbolRepository)

        self.command = CreateSymbolCommand(self.symbol_repository)

    def test_execute(self) -> None:
        symbol = Symbol(name="Ethereum", symbol="ETH")
        created_symbol = Symbol(id=2, name="Ethereum", symbol="ETH")
        self.symbol_repository.insert.return_value = created_symbol

        result = self.command.execute(symbol)

        self.assertEqual(
            CreateSymbolCommandResponse(created_symbol=created_symbol), result
        )
        self.symbol_repository.insert.assert_called_once_with(symbol)
