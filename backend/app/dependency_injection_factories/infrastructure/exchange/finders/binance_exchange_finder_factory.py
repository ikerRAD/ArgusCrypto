from app.dependency_injection_factories.infrastructure.exchange.database.repositories import (
    DbExchangeRepositoryFactory,
)
from app.infrastructure.exchange.finders.binance_exchange_finder import (
    BinanceExchangeFinder,
)


class BinanceExchangeFinderFactory:
    @staticmethod
    def create() -> BinanceExchangeFinder:
        return BinanceExchangeFinder(
            DbExchangeRepositoryFactory.create(),
        )
