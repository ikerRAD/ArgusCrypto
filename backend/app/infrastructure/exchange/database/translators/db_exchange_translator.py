from app.domain.exchange.models.exchange import Exchange
from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)
from app.infrastructure.exchange.database.table_models import ExchangeTableModel


class DbExchangeTranslator:
    def __init__(self, db_ticker_translator: DbTickerTranslator):
        self.__db_ticker_translator = db_ticker_translator

    def translate_to_domain_model(
        self, exchange_table_model: ExchangeTableModel, with_tickers=False
    ) -> Exchange:
        domain_exchange = Exchange(
            id=exchange_table_model.id,
            name=exchange_table_model.name,
        )

        if with_tickers:
            domain_exchange.tickers = (
                self.__db_ticker_translator.bulk_translate_to_domain_model(
                    exchange_table_model.tickers
                )
            )

        return domain_exchange
