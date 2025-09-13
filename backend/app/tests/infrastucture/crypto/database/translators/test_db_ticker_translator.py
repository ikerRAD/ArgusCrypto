from unittest import TestCase

from app.infrastructure.crypto.database.table_models import TickerTableModel
from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)


class TestDbTickerTranslator(TestCase):
    def setUp(self) -> None:
        self.translator = DbTickerTranslator()

    def test_translate_to_domain_model(self) -> None:
        ticker_table_model = TickerTableModel(
            id=1, symbol_id=1, exchange_id=1, ticker="SOME"
        )

        result = self.translator.translate_to_domain_model(ticker_table_model)

        self.assertEqual(result.id, 1)
        self.assertEqual(result.symbol_id, 1)
        self.assertEqual(result.ticker, "SOME")
        self.assertEqual(result.exchange_id, 1)

    def test_bulk_translate_to_domain_model(self) -> None:
        first_ticker_table_model = TickerTableModel(
            id=1, symbol_id=1, exchange_id=1, ticker="SOME"
        )
        second_ticker_table_model = TickerTableModel(
            symbol_id=2, exchange_id=2, ticker="OTHER"
        )
        third_ticker_table_model = TickerTableModel(
            id=3, symbol_id=2, exchange_id=1, ticker="TICKER"
        )

        result = self.translator.bulk_translate_to_domain_model(
            [
                first_ticker_table_model,
                second_ticker_table_model,
                third_ticker_table_model,
            ]
        )

        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].symbol_id, 1)
        self.assertEqual(result[0].ticker, "SOME")
        self.assertEqual(result[0].exchange_id, 1)
        self.assertIsNone(result[1].id)
        self.assertEqual(result[1].symbol_id, 2)
        self.assertEqual(result[1].ticker, "OTHER")
        self.assertEqual(result[1].exchange_id, 2)
        self.assertEqual(result[2].id, 3)
        self.assertEqual(result[2].symbol_id, 2)
        self.assertEqual(result[2].ticker, "TICKER")
        self.assertEqual(result[2].exchange_id, 1)
