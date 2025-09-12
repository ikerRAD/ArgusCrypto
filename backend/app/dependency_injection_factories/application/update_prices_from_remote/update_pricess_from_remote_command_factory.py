from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.dependency_injection_factories.infrastructure.crypto.repositories.db_price_repository_factory import (
    DbPriceRepositoryFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.clients.binance_client_factory import (
    BinanceClientFactory,
)
from app.dependency_injection_factories.infrastructure.exchange.repositories.db_binance_repository_factory import (
    DbBinanceRepositoryFactory,
)


class UpdatePricesFromRemoteCommandFactory:
    @staticmethod
    def create_for_binance() -> UpdatePricesFromRemoteCommand:
        return UpdatePricesFromRemoteCommand(
            BinanceClientFactory.create(),
            DbBinanceRepositoryFactory.create(),
            DbPriceRepositoryFactory.create(),
        )
