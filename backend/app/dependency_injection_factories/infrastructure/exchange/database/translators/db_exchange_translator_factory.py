from app.dependency_injection_factories.infrastructure.crypto.database.translators.db_ticker_translator_factory import (
    DbTickerTranslatorFactory,
)
from app.infrastructure.exchange.database.translators.db_exchange_translator import (
    DbExchangeTranslator,
)


class DbExchangeTranslatorFactory:
    @staticmethod
    def create() -> DbExchangeTranslator:
        return DbExchangeTranslator(DbTickerTranslatorFactory.create())
