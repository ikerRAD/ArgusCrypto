from app.dependency_injection_factories.infrastructure.crypto.database.translators.db_symbol_translator_factory import (
    DbSymbolTranslatorFactory,
)
from app.infrastructure.crypto.database.repositories.db_symbol_repository import (
    DbSymbolRepository,
)


class DbSymbolRepositoryFactory:
    @staticmethod
    def create() -> DbSymbolRepository:
        return DbSymbolRepository(DbSymbolTranslatorFactory.create())
