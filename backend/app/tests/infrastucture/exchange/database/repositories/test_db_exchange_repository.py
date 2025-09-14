from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import Result
from sqlalchemy.orm import Session

from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models.exchange import Exchange
from app.infrastructure.exchange.database.repositories.db_exchange_repository import (
    DbExchangeRepository,
)
from app.infrastructure.exchange.database.table_models import ExchangeTableModel
from app.infrastructure.exchange.database.translators.db_exchange_translator import (
    DbExchangeTranslator,
)


class TestDbExchangeRepository(TestCase):
    def setUp(self) -> None:
        self.exchange = Exchange(name="Binance")
        self.exchange_table_model = ExchangeTableModel(name="Binance")
        self.db_exchange_translator = Mock(spec=DbExchangeTranslator)

        self.repository = DbExchangeRepository(self.db_exchange_translator)

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_or_fail_by_name(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = self.exchange_table_model
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session
        self.db_exchange_translator.translate_to_domain_model.return_value = (
            self.exchange
        )

        result = self.repository.get_or_fail_by_name("Binance", False)

        self.assertEqual(result, self.exchange)
        self.assertEqual(result.tickers, None)
        self.db_exchange_translator.translate_to_domain_model.assert_called_once_with(
            self.exchange_table_model, False
        )
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_or_fail_by_name_fetching_tickers(self, get_session: Mock) -> None:
        tickers = [
            Ticker(symbol_id=1, exchange_id=1, ticker="SOME"),
            Ticker(symbol_id=2, exchange_id=1, ticker="OTHER"),
            Ticker(symbol_id=3, exchange_id=1, ticker="TICKER"),
            Ticker(symbol_id=4, exchange_id=1, ticker="HERE"),
        ]
        self.exchange.tickers = tickers
        self.db_exchange_translator.translate_to_domain_model.return_value = (
            self.exchange
        )
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = self.exchange_table_model
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        result = self.repository.get_or_fail_by_name("Binance", True)

        self.assertEqual(result, self.exchange)
        self.assertEqual(result.tickers, tickers)
        self.db_exchange_translator.translate_to_domain_model.assert_called_once_with(
            self.exchange_table_model, True
        )
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_or_fail_by_name_not_found(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = None
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        with self.assertRaisesRegex(
            ExchangeNotFoundException, "exchange with name 'Some' not found'"
        ):
            self.repository.get_or_fail_by_name("Some", False)

        self.db_exchange_translator.translate_to_domain_model.assert_not_called()
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_all(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalars.return_value.all.return_value = [self.exchange_table_model]
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session
        self.db_exchange_translator.bulk_translate_to_domain_model.return_value = [
            self.exchange
        ]

        result = self.repository.get_all()

        self.assertEqual(result, [self.exchange])
        self.db_exchange_translator.bulk_translate_to_domain_model.assert_called_once_with(
            [self.exchange_table_model]
        )
        query_result.scalars.assert_called_once()
        query_result.scalars.return_value.all.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_or_fail_by_id(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = self.exchange_table_model
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session
        self.db_exchange_translator.translate_to_domain_model.return_value = (
            self.exchange
        )

        result = self.repository.get_or_fail_by_id(1)

        self.assertEqual(result, self.exchange)
        self.assertEqual(result.tickers, None)
        self.db_exchange_translator.translate_to_domain_model.assert_called_once_with(
            self.exchange_table_model
        )
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.exchange.database.repositories.db_exchange_repository.get_session"
    )
    def test_get_or_fail_by_id_not_found(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = None
        session = Mock(spec=Session)
        session.execute.return_value = query_result
        get_session.return_value.__enter__.return_value = session

        with self.assertRaisesRegex(
            ExchangeNotFoundException, "exchange with id '1000' not found'"
        ):
            self.repository.get_or_fail_by_id(1000)

        self.db_exchange_translator.translate_to_domain_model.assert_not_called()
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()
