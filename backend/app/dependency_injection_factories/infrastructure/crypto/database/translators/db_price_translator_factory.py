from app.infrastructure.crypto.database.translators.db_price_translator import (
    DbPriceTranslator,
)


class DbPriceTranslatorFactory:
    @staticmethod
    def create() -> DbPriceTranslator:
        return DbPriceTranslator()
