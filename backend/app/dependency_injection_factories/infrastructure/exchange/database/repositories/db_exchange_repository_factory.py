from app.dependency_injection_factories.infrastructure.exchange.database.translators.db_exchange_translator_factory import (
    DbExchangeTranslatorFactory,
)
from app.infrastructure.exchange.database.repositories.db_exchange_repository import (
    DbExchangeRepository,
)


class DbExchangeRepositoryFactory:
    @staticmethod
    def create() -> DbExchangeRepository:
        return DbExchangeRepository(DbExchangeTranslatorFactory.create())
