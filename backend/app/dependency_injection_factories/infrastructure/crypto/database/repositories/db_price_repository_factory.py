from app.dependency_injection_factories.infrastructure.crypto.database.translators.db_price_translator_factory import (
    DbPriceTranslatorFactory,
)
from app.infrastructure.crypto.database.repositories.db_price_repository import (
    DbPriceRepository,
)


class DbPriceRepositoryFactory:
    @staticmethod
    def create() -> DbPriceRepository:
        return DbPriceRepository(DbPriceTranslatorFactory.create())
