from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import Result
from sqlalchemy.orm import Session

from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.price import Price
from app.infrastructure.crypto.database.repositories.db_price_repository import (
    DbPriceRepository,
)
from app.infrastructure.crypto.database.table_models import (
    PriceTableModel,
)
from app.infrastructure.crypto.database.translators.db_price_translator import (
    DbPriceTranslator,
)


class TestDbPriceRepository(TestCase):
    def setUp(self) -> None:
        self.start_date = datetime(2020, 1, 1)
        self.end_date = datetime(2020, 12, 31)
        self.domain_prices = [
            Price(ticker_id=1, price=1.0),
            Price(ticker_id=1, price=2.0),
            Price(ticker_id=1, price=3.0),
        ]
        self.price_table_models = [
            PriceTableModel(ticker_id=1, price=1.0),
            PriceTableModel(ticker_id=1, price=2.0),
            PriceTableModel(ticker_id=1, price=3.0),
        ]
        self.db_price_translator = Mock(spec=DbPriceTranslator)

        self.repository = DbPriceRepository(self.db_price_translator)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_price_repository.get_session"
    )
    def test_bulk_save(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        self.db_price_translator.bulk_translate_to_table_model.return_value = (
            self.price_table_models
        )

        self.repository.bulk_save(self.domain_prices)

        self.db_price_translator.bulk_translate_to_table_model.assert_called_once_with(
            self.domain_prices
        )
        session.add_all.assert_called_once_with(self.price_table_models)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_price_repository.get_session"
    )
    def test_get_all_or_fail_by_ticker_id(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_query_result = Mock(spec=Result)
        query_result = Mock(spec=Result)
        query_result.scalars.return_value.all.return_value = self.price_table_models
        session.execute.side_effect = [ticker_query_result, query_result]
        self.db_price_translator.bulk_translate_to_domain_model.return_value = (
            self.domain_prices
        )

        result = self.repository.get_all_or_fail_by_ticker_id(
            1, self.start_date, self.start_date
        )

        self.assertEqual(self.domain_prices, result)
        self.assertEqual(2, session.execute.call_count)
        self.db_price_translator.bulk_translate_to_domain_model.assert_called_once_with(
            self.price_table_models
        )

    @patch(
        "app.infrastructure.crypto.database.repositories.db_price_repository.get_session"
    )
    def test_get_all_or_fail_by_ticker_id_not_found(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        ticker_query_result = Mock(spec=Result)
        ticker_query_result.scalar_one_or_none.return_value = None
        session.execute.return_value = ticker_query_result

        with self.assertRaisesRegex(
            TickerNotFoundException, "Ticker with id '1000' not found."
        ):
            self.repository.get_all_or_fail_by_ticker_id(
                1000, self.start_date, self.start_date
            )

        session.execute.assert_called_once()
        self.db_price_translator.bulk_translate_to_domain_model.assert_not_called()

    @patch(
        "app.infrastructure.crypto.database.repositories.db_price_repository.get_session"
    )
    def test_get_all_or_fail_by_ticker_id_ignore_ticker(
        self, get_session: Mock
    ) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        query_result = Mock(spec=Result)
        query_result.scalars.return_value.all.return_value = self.price_table_models
        session.execute.return_value = query_result
        self.db_price_translator.bulk_translate_to_domain_model.return_value = (
            self.domain_prices
        )

        result = self.repository.get_all_or_fail_by_ticker_id(
            1000, self.start_date, self.start_date, check_ticker=False
        )

        self.assertEqual(self.domain_prices, result)
        session.execute.assert_called_once()
        self.db_price_translator.bulk_translate_to_domain_model.assert_called_once_with(
            self.price_table_models
        )
