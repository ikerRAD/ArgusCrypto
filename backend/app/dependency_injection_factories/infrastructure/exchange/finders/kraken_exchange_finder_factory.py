from app.dependency_injection_factories.infrastructure.exchange.database.repositories.db_exchange_repository_factory import (
    DbExchangeRepositoryFactory,
)
from app.infrastructure.exchange.finders.kraken_exchange_finder import (
    KrakenExchangeFinder,
)


class KrakenExchangeFinderFactory:
    @staticmethod
    def create() -> KrakenExchangeFinder:
        return KrakenExchangeFinder(DbExchangeRepositoryFactory.create())
