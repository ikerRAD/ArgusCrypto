from unittest import TestCase

from app.domain.crypto.models.price import Price
from app.infrastructure.crypto.database.table_models import PriceTableModel
from app.infrastructure.crypto.database.translators.db_price_translator import (
    DbPriceTranslator,
)


class TestDbPriceTranslator(TestCase):
    def setUp(self) -> None:
        self.translator = DbPriceTranslator()

    def test_translate_to_table_model(self) -> None:
        domain_price = Price(ticker_id=1, price=5.0)

        result = self.translator.translate_to_table_model(domain_price)

        self.assertEqual(result.price, 5.0)
        self.assertEqual(result.ticker_id, 1)
        self.assertIsNone(result.id)
        self.assertEqual(result.timestamp, result.timestamp)

    def test_translate_to_table_model_with_id(self) -> None:
        domain_price = Price(id=10, ticker_id=1, price=5.0)

        result = self.translator.translate_to_table_model(domain_price)

        self.assertEqual(result.price, 5.0)
        self.assertEqual(result.ticker_id, 1)
        self.assertEqual(result.id, 10)
        self.assertEqual(result.timestamp, result.timestamp)

    def test_bulk_translate_to_table_model(self) -> None:
        first_domain_price = Price(id=10, ticker_id=1, price=5.0)
        second_domain_price = Price(ticker_id=1, price=5.1)
        third_domain_price = Price(id=15, ticker_id=1, price=4.9)

        result = self.translator.bulk_translate_to_table_model(
            [first_domain_price, second_domain_price, third_domain_price]
        )

        self.assertEqual(result[0].price, 5.0)
        self.assertEqual(result[0].ticker_id, 1)
        self.assertEqual(result[0].id, 10)
        self.assertEqual(result[0].timestamp, result[0].timestamp)
        self.assertEqual(result[1].price, 5.1)
        self.assertEqual(result[1].ticker_id, 1)
        self.assertIsNone(result[1].id)
        self.assertEqual(result[1].timestamp, result[0].timestamp)
        self.assertEqual(result[2].price, 4.9)
        self.assertEqual(result[2].ticker_id, 1)
        self.assertEqual(result[2].id, 15)
        self.assertEqual(result[2].timestamp, result[0].timestamp)

    def test_translate_to_domain_model(self) -> None:
        price_table_model = PriceTableModel(ticker_id=1, price=5.0)

        result = self.translator.translate_to_domain_model(price_table_model)

        self.assertEqual(result.price, 5.0)
        self.assertEqual(result.ticker_id, 1)
        self.assertIsNone(result.id)
        self.assertEqual(result.timestamp, result.timestamp)

    def test_bulk_translate_to_domain_model(self) -> None:
        first_price_table_model = PriceTableModel(id=10, ticker_id=1, price=5.0)
        second_price_table_model = PriceTableModel(ticker_id=1, price=5.1)
        third_price_table_model = PriceTableModel(id=15, ticker_id=1, price=4.9)

        result = self.translator.bulk_translate_to_table_model(
            [first_price_table_model, second_price_table_model, third_price_table_model]
        )

        self.assertEqual(result[0].price, 5.0)
        self.assertEqual(result[0].ticker_id, 1)
        self.assertEqual(result[0].id, 10)
        self.assertEqual(result[0].timestamp, result[0].timestamp)
        self.assertEqual(result[1].price, 5.1)
        self.assertEqual(result[1].ticker_id, 1)
        self.assertIsNone(result[1].id)
        self.assertEqual(result[1].timestamp, result[0].timestamp)
        self.assertEqual(result[2].price, 4.9)
        self.assertEqual(result[2].ticker_id, 1)
        self.assertEqual(result[2].id, 15)
        self.assertEqual(result[2].timestamp, result[0].timestamp)
