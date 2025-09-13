from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy.orm import Session

from app.domain.crypto.models.price import Price
from app.infrastructure.crypto.database.repositories.db_price_repository import (
    DbPriceRepository,
)
from app.infrastructure.crypto.database.table_models import PriceTableModel
from app.infrastructure.crypto.database.translators.db_price_translator import (
    DbPriceTranslator,
)


class TestDbPriceRepository(TestCase):
    def setUp(self) -> None:
        self.db_price_translator = Mock(spec=DbPriceTranslator)

        self.repository = DbPriceRepository(self.db_price_translator)

    @patch(
        "app.infrastructure.crypto.database.repositories.db_price_repository.get_session"
    )
    def test_bulk_save(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session
        domain_prices = [
            Price(ticker_id=1, price=1.0),
            Price(ticker_id=1, price=2.0),
            Price(ticker_id=1, price=3.0),
        ]
        price_table_models = [
            PriceTableModel(ticker_id=1, price=1.0),
            PriceTableModel(ticker_id=1, price=2.0),
            PriceTableModel(ticker_id=1, price=3.0),
        ]
        self.db_price_translator.bulk_translate_to_table_model.return_value = (
            price_table_models
        )

        self.repository.bulk_save(domain_prices)

        self.db_price_translator.bulk_translate_to_table_model.assert_called_once_with(
            domain_prices
        )
        session.add_all.assert_called_once_with(price_table_models)
