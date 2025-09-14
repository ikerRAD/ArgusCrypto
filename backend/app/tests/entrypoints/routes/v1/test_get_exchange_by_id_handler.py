from unittest import TestCase
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.application.get_exchange_by_id.get_exchange_by_id_query import (
    GetExchangeByIdQuery,
)
from app.application.get_exchange_by_id.get_exchange_by_id_query_response import (
    GetExchangeByIdQueryResponse,
)
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models.exchange import Exchange
from app.entrypoints.routes.v1.get_exchange_by_id_handler import GetExchangeByIdHandler
from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema


class TestGetExchangeByIdHandler(TestCase):
    def setUp(self) -> None:
        self.get_exchange_by_id_query = Mock(spec=GetExchangeByIdQuery)

        self.handler = GetExchangeByIdHandler(self.get_exchange_by_id_query)

    @patch("app.entrypoints.routes.v1.get_exchange_by_id_handler.logger")
    def test_handle(self, logger: Mock) -> None:
        query_response = GetExchangeByIdQueryResponse(
            exchange=Exchange(id=1, name="test")
        )
        self.get_exchange_by_id_query.execute.return_value = query_response

        result = self.handler.handle(1)

        self.assertEqual(ExchangeSchema(id=1, name="test"), result)
        logger.info.assert_called_once_with(
            "Getting exchange with id '1' from database"
        )
        logger.error.assert_not_called()

    @patch("app.entrypoints.routes.v1.get_exchange_by_id_handler.logger")
    def test_handle_not_found(self, logger: Mock) -> None:
        self.get_exchange_by_id_query.execute.side_effect = ExchangeNotFoundException(
            "id", 12
        )

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(12)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(context.exception.detail, "Exchange not found")
            logger.error.assert_called_once_with("Exchange with id '12' not found")

        logger.info.assert_called_once_with(
            "Getting exchange with id '12' from database"
        )

    @patch("app.entrypoints.routes.v1.get_exchange_by_id_handler.logger")
    def test_handle_unexpected_error(self, logger: Mock) -> None:
        self.get_exchange_by_id_query.execute.side_effect = Exception()

        with self.assertRaises(HTTPException) as context:
            self.handler.handle(1)

            self.assertEqual(context.exception.status_code, 500)
            self.assertEqual(context.exception.detail, "An unexpected error happened.")
            logger.error.assert_called_once_with(
                f"Unexpected error occurred while retrieving exchange with id '1': {context.exception}"
            )

        logger.info.assert_called_once_with(
            "Getting exchange with id '1' from database"
        )
