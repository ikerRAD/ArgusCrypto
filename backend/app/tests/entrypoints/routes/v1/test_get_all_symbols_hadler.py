from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_all_symbols.get_all_symbols_query import GetAllSymbolsQuery
from app.application.get_all_symbols.get_all_symbols_query_response import (
    GetAllSymbolsQueryResponse,
)
from app.domain.crypto.models.symbol import Symbol
from app.entrypoints.routes.v1.get_all_symbols_handler import GetAllSymbolsHandler
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema


class TestGetAllSymbolsHandler(TestCase):
    def setUp(self) -> None:
        self.get_all_symbols_query = Mock(spec=GetAllSymbolsQuery)

        self.handler = GetAllSymbolsHandler(self.get_all_symbols_query)

    @patch("app.entrypoints.routes.v1.get_all_symbols_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        symbol_schemas = [SymbolSchema(id=1, name="test", symbol="TST")]
        domain_schemas = [Symbol(id=1, name="test", symbol="TST")]
        self.get_all_symbols_query.execute.return_value = GetAllSymbolsQueryResponse(
            symbols=domain_schemas
        )

        result = self.handler.handle()

        self.assertEqual(result, symbol_schemas)
        self.get_all_symbols_query.execute.assert_called_once()
        logger.info.assert_called_once_with("Getting all symbols from database")
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_all_symbols_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_all_symbols_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle()

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"An unexpected error happened while retrieving all symbols: {context.exception}"
            )

        self.get_all_symbols_query.execute.assert_called_once()
        logger.info.assert_called_once_with("Getting all symbols from database")
