from app.infrastructure.crypto.database.translators.db_symbol_translator import (
    DbSymbolTranslator,
)


class DbSymbolTranslatorFactory:
    @staticmethod
    def create() -> DbSymbolTranslator:
        return DbSymbolTranslator()
