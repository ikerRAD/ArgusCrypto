from app.application.create_ticker.create_ticker_command import CreateTickerCommand
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_ticker_repository_factory import (
    DbTickerRepositoryFactory,
)


class CreateTickerCommandFactory:
    @staticmethod
    def create() -> CreateTickerCommand:
        return CreateTickerCommand(DbTickerRepositoryFactory.create())
