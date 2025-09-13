from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)


class DbTickerTranslatorFactory:
    @staticmethod
    def create() -> DbTickerTranslator:
        return DbTickerTranslator()
