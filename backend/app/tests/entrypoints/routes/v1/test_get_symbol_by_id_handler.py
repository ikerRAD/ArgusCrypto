from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_symbol_by_id.get_symbol_by_id_query import GetSymbolByIdQuery
from app.application.get_symbol_by_id.get_symbol_by_id_query_response import (
    GetSymbolByIdQueryResponse,
)
from app.domain.crypto.exceptions.symbol_not_found_exception import (
    SymbolNotFoundException,
)
from app.domain.crypto.models.symbol import Symbol
from app.entrypoints.routes.v1.get_symbol_by_id_handler import GetSymbolByIdHandler
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema


class TestGetSymbolByIdHandler(TestCase):
    def setUp(self) -> None:
        self.query = Mock(spec=GetSymbolByIdQuery)

        self.handler = GetSymbolByIdHandler(self.query)

    @patch("app.entrypoints.routes.v1.get_symbol_by_id_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        query_response = GetSymbolByIdQueryResponse(
            symbol=Symbol(id=1, name="test", symbol="TST")
        )
        self.query.execute.return_value = query_response

        result = self.handler.handle(1)

        self.assertEqual(SymbolSchema(id=1, name="test", symbol="TST"), result)
        logger.info.assert_called_once_with("Getting symbol with id '1' from database")
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_symbol_by_id_handler.logger")
    def test_handle_not_found(self, logger: Mock) -> None:
        self.query.execute.side_effect = SymbolNotFoundException(12)

        with self.assertRaises(HTTPException) as e:
            self.handler.handle(12)

            self.assertEqual(e.exception.status_code, 404)
            self.assertEqual(e.exception.detail, "Symbol not found")
            logger.error.assert_called_once_with("Symbol with id '12' not found")

        logger.info.assert_called_once_with("Getting symbol with id '12' from database")

    @patch("app.entrypoints.routes.v1.get_symbol_by_id_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as e:
            self.handler.handle(1)

            self.assertEqual(e.exception.status_code, 500)
            self.assertEqual(e.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"Unexpected error occurred while retrieving symbol with id '1': {e.exception}"
            )

        logger.info.assert_called_once_with("Getting symbol with id '1' from database")
