from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.create_symbol.create_symbol_command import CreateSymbolCommand
from app.application.create_symbol.create_symbol_command_response import (
    CreateSymbolCommandResponse,
)
from app.domain.crypto.exceptions.symbol_already_exists_exception import (
    SymbolAlreadyExistsException,
)
from app.domain.crypto.models.symbol import Symbol
from app.entrypoints.routes.v1.post_symbol_handler import PostSymbolHandler
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema


class TestPostSymbolHandler(TestCase):
    def setUp(self) -> None:
        self.create_symbol_command = Mock(spec=CreateSymbolCommand)

        self.handler = PostSymbolHandler(self.create_symbol_command)

    @patch("app.entrypoints.routes.v1.post_symbol_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        command_response = CreateSymbolCommandResponse(
            created_symbol=Symbol(id=1, name="test", symbol="TST")
        )
        self.create_symbol_command.execute.return_value = command_response
        symbol_create = SymbolCreateSchema(name="test", symbol="TST")

        result = self.handler.handle(symbol_create)

        self.assertEqual(result, SymbolSchema(id=1, name="test", symbol="TST"))
        self.create_symbol_command.execute.assert_called_once_with(
            Symbol(name="test", symbol="TST")
        )
        logger.info.assert_called_once_with("Creating symbol 'TST'")
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.post_symbol_handler.logger")
    def test_handle_symbol_exists(self, logger: Mock) -> None:
        self.create_symbol_command.execute.side_effect = SymbolAlreadyExistsException(
            "BTC"
        )
        symbol_create = SymbolCreateSchema(name="Bitcoin", symbol="BTC")

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(symbol_create)

            self.assertEqual(context.exception.status_code, 409)
            self.assertEqual(context.exception.detail, "Symbol 'BTC' already exists")
            logger.error.assert_called_once_with("Symbol 'BTC' already exists")

        self.create_symbol_command.execute.assert_called_once_with(
            Symbol(name="Bitcoin", symbol="BTC")
        )
        logger.info.assert_called_once_with("Creating symbol 'BTC'")

    @patch("app.entrypoints.routes.v1.post_symbol_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.create_symbol_command.execute.side_effect = Exception()
        symbol_create = SymbolCreateSchema(name="test", symbol="TST")

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(symbol_create)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"An unexpected error happened creating the symbol 'TST': {context.exception}"
            )

        self.create_symbol_command.execute.assert_called_once_with(
            Symbol(name="test", symbol="TST")
        )
        logger.info.assert_called_once_with("Creating symbol 'TST'")
