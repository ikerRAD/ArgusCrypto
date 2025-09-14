from app.dependency_injection_factories.infrastructure.crypto.database.translators.db_ticker_translator_factory import (
    DbTickerTranslatorFactory,
)
from app.infrastructure.crypto.database.repositories.db_ticker_repository import (
    DbTickerRepository,
)


class DbTickerRepositoryFactory:
    @staticmethod
    def create() -> DbTickerRepository:
        return DbTickerRepository(DbTickerTranslatorFactory.create())
