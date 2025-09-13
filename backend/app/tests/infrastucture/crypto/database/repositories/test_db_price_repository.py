from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy.orm import Session

from app.domain.crypto.models.price import Price
from app.infrastructure.crypto.database.repositories.db_price_repository import DbPriceRepository


class TestDbPriceRepository(TestCase):
    def setUp(self) -> None:
        self.repository = DbPriceRepository()

    @patch("app.infrastructure.crypto.repositories.db_price_repository.get_session")
    def test_bulk_save(self, get_session: Mock) -> None:
        session = Mock(spec=Session)
        get_session.return_value.__enter__.return_value = session

        prices = [
            Price(ticker_id=1, price=1.0),
            Price(ticker_id=1, price=2.0),
            Price(ticker_id=1, price=3.0),
        ]

        self.repository.bulk_save(prices)

        session.add_all.assert_called_once_with(prices)
