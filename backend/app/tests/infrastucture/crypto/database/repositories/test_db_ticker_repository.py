from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.crypto.exceptions.reference_to_non_existent_id_exception import (
    ReferenceToNonExistentIdException,
)
from app.domain.crypto.exceptions.ticker_already_exists_exception import (
    TickerAlreadyExistsException,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.infrastructure.crypto.database.repositories.db_ticker_repository import (
    DbTickerRepository,
)
from app.infrastructure.crypto.database.table_models import TickerTableModel
from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)


class TestDbTickerRepository(TestCase):
    def setUp(self) -> None:
        self.db_ticker_translator = Mock(spec=DbTickerTranslator)

        self.repository = DbTickerRepository(self.db_ticker_translator)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_get_all_or_fail_by_exchange_id(self, get_session: Mock) -> None:
        ticker_table_models = [
            TickerTableModel(id=1, ticker="BTCUSDT", symbol_id=1, exchange_id=1),
            TickerTableModel(id=1, ticker="BTCEUR", symbol_id=1, exchange_id=1),
        ]
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value.tickers = ticker_table_models
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        session.execute.return_value = query_result
        tickers = [
            Ticker(id=1, ticker="BTCUSDT", symbol_id=1, exchange_id=1),
            Ticker(id=1, ticker="BTCEUR", symbol_id=1, exchange_id=1),
        ]
        self.db_ticker_translator.bulk_translate_to_domain_model.return_value = tickers

        result = self.repository.get_all_or_fail_by_exchange_id(1)

        self.assertEqual(tickers, result)
        self.db_ticker_translator.bulk_translate_to_domain_model.assert_called_once_with(
            ticker_table_models
        )
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_get_all_or_fail_by_exchange_id_not_found(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = None
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        session.execute.return_value = query_result

        with self.assertRaisesRegex(
            ExchangeNotFoundException, "exchange with id '1000' not found"
        ):
            self.repository.get_all_or_fail_by_exchange_id(1000)

        self.db_ticker_translator.translate_to_domain_model.assert_not_called()
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_get_or_fail_by_id(self, get_session: Mock) -> None:
        ticker_table_model = TickerTableModel(
            id=1, ticker="BTCUSDT", symbol_id=1, exchange_id=1
        )
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = ticker_table_model
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        session.execute.return_value = query_result
        ticker = Ticker(id=1, ticker="BTCUSDT", symbol_id=1, exchange_id=1)
        self.db_ticker_translator.translate_to_domain_model.return_value = ticker

        result = self.repository.get_or_fail_by_id(1)

        self.assertEqual(ticker, result)
        self.db_ticker_translator.translate_to_domain_model.assert_called_once_with(
            ticker_table_model
        )
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_get_or_fail_by_id_not_found(self, get_session: Mock) -> None:
        query_result = Mock(spec=Result)
        query_result.scalar_one_or_none.return_value = None
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        session.execute.return_value = query_result

        with self.assertRaisesRegex(
            TickerNotFoundException, "Ticker with id '1000' not found"
        ):
            self.repository.get_or_fail_by_id(1000)

        self.db_ticker_translator.translate_to_domain_model.assert_not_called()
        query_result.scalar_one_or_none.assert_called_once()
        session.execute.assert_called_once()

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_insert(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_table_model = TickerTableModel(
            ticker="BTCUSDT", symbol_id=1, exchange_id=1
        )
        self.db_ticker_translator.translate_to_table_model.return_value = (
            ticker_table_model
        )
        ticker = Ticker(ticker="BTCUSDT", symbol_id=1, exchange_id=1)

        self.repository.insert(ticker)

        self.db_ticker_translator.translate_to_table_model.assert_called_once_with(
            ticker
        )
        self.db_ticker_translator.translate_to_domain_model.assert_called_once_with(
            ticker_table_model
        )
        session.add.assert_called_once_with(ticker_table_model)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_insert_already_exists(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_table_model = TickerTableModel(
            ticker="BTCUSDT", symbol_id=1, exchange_id=1
        )
        self.db_ticker_translator.translate_to_table_model.return_value = (
            ticker_table_model
        )
        ticker = Ticker(ticker="BTCUSDT", symbol_id=1, exchange_id=1)
        session.add.side_effect = IntegrityError(
            "violated unique constraint",
            None,
            Exception("unique_exchange_ticker constraint violated"),
        )

        with self.assertRaisesRegex(
            TickerAlreadyExistsException,
            "Ticker 'BTCUSDT' already exists for exchange '1'",
        ):
            self.repository.insert(ticker)

        self.db_ticker_translator.translate_to_table_model.assert_called_once_with(
            ticker
        )
        self.db_ticker_translator.translate_to_domain_model.assert_not_called()
        session.add.assert_called_once_with(ticker_table_model)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_insert_symbol_id_not_exists(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_table_model = TickerTableModel(
            ticker="BTCUSDT", symbol_id=13, exchange_id=1
        )
        self.db_ticker_translator.translate_to_table_model.return_value = (
            ticker_table_model
        )
        ticker = Ticker(ticker="BTCUSDT", symbol_id=13, exchange_id=1)
        session.add.side_effect = IntegrityError(
            "value not present",
            None,
            Exception('Key (symbol_id)=(13) is not present in table "exchanges".'),
        )

        with self.assertRaisesRegex(
            ReferenceToNonExistentIdException, "symbol_id '13' is non-existent"
        ):
            self.repository.insert(ticker)

        self.db_ticker_translator.translate_to_table_model.assert_called_once_with(
            ticker
        )
        self.db_ticker_translator.translate_to_domain_model.assert_not_called()
        session.add.assert_called_once_with(ticker_table_model)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_ticker_repository.get_session"
    )
    def test_insert_exchange_id_not_exists(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_table_model = TickerTableModel(
            ticker="BTCUSDT", symbol_id=1, exchange_id=13
        )
        self.db_ticker_translator.translate_to_table_model.return_value = (
            ticker_table_model
        )
        ticker = Ticker(ticker="BTCUSDT", symbol_id=1, exchange_id=13)
        session.add.side_effect = IntegrityError(
            "value not present",
            None,
            Exception('Key (exchange_id)=(13) is not present in table "exchanges".'),
        )

        with self.assertRaisesRegex(
            ReferenceToNonExistentIdException, "exchange_id '13' is non-existent"
        ):
            self.repository.insert(ticker)

        self.db_ticker_translator.translate_to_table_model.assert_called_once_with(
            ticker
        )
        self.db_ticker_translator.translate_to_domain_model.assert_not_called()
        session.add.assert_called_once_with(ticker_table_model)
