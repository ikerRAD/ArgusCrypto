from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.dependency_injection_factories.infrastructure.crypto.repositories.db_price_repository_factory import (
    DbPriceRepositoryFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.clients.binance_client_factory import (
    BinanceClientFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.clients.kraken_client_factory import (
    KrakenClientFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.finders.binance_exchange_finder_factory import (
    BinanceExchangeFinderFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.finders.kraken_exchange_finder_factory import (
    KrakenExchangeFinderFactory,
)


class UpdatePricesFromRemoteCommandFactory:
    @staticmethod
    def create_for_binance() -> UpdatePricesFromRemoteCommand:
        return UpdatePricesFromRemoteCommand(
            BinanceClientFactory.create(),
            BinanceExchangeFinderFactory.create(),
            DbPriceRepositoryFactory.create(),
        )

    @staticmethod
    def create_for_kraken() -> UpdatePricesFromRemoteCommand:
        return UpdatePricesFromRemoteCommand(
            KrakenClientFactory.create(),
            KrakenExchangeFinderFactory.create(),
            DbPriceRepositoryFactory.create(),
        )
