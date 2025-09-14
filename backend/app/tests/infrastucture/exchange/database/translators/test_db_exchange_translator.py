from unittest import TestCase
from unittest.mock import Mock

from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.models.exchange import Exchange
from app.infrastructure.crypto.database.table_models import TickerTableModel
from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)
from app.infrastructure.exchange.database.table_models import ExchangeTableModel
from app.infrastructure.exchange.database.translators.db_exchange_translator import (
    DbExchangeTranslator,
)


class TestDbExchangeTranslator(TestCase):
    def setUp(self) -> None:
        self.db_ticker_translator = Mock(spec=DbTickerTranslator)

        self.translator = DbExchangeTranslator(self.db_ticker_translator)

    def test_translate_to_domain_model(self) -> None:
        exchange_table_model = ExchangeTableModel(name="Kraken")
        expected_domain_exchange = Exchange(name="Kraken")

        result = self.translator.translate_to_domain_model(exchange_table_model)

        self.assertEqual(result, expected_domain_exchange)
        self.db_ticker_translator.bulk_translate_to_domain_model.assert_not_called()

    def test_translate_to_domain_model_with_tickers(self) -> None:
        ticker_table_models = [
            TickerTableModel(symbol_id=1, exchange_id=2, ticker="SOME")
        ]
        exchange_table_model = Mock(spec=ExchangeTableModel)
        exchange_table_model.name = "Kraken"
        exchange_table_model.id = None
        exchange_table_model.tickers = ticker_table_models
        domain_tickers = [Ticker(symbol_id=1, exchange_id=2, ticker="SOME")]
        expected_domain_exchange = Exchange(name="Kraken", tickers=domain_tickers)
        self.db_ticker_translator.bulk_translate_to_domain_model.return_value = (
            domain_tickers
        )

        result = self.translator.translate_to_domain_model(
            exchange_table_model, with_tickers=True
        )

        self.assertEqual(result, expected_domain_exchange)
        self.db_ticker_translator.bulk_translate_to_domain_model.assert_called_once_with(
            ticker_table_models
        )

    def test_bulk_translate_to_domain_model(self) -> None:
        exchange_table_models = [
            ExchangeTableModel(name="Kraken"),
            ExchangeTableModel(id=1, name="Binance"),
        ]
        expected_domain_exchanges = [
            Exchange(name="Kraken"),
            Exchange(id=1, name="Binance"),
        ]

        result = self.translator.bulk_translate_to_domain_model(exchange_table_models)

        self.assertEqual(result, expected_domain_exchanges)
        self.db_ticker_translator.bulk_translate_to_domain_model.assert_not_called()
