from app.application.create_symbol.create_symbol_command import CreateSymbolCommand
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_symbol_repository_factory import (
    DbSymbolRepositoryFactory,
)


class CreateSymbolCommandFactory:
    @staticmethod
    def create() -> CreateSymbolCommand:
        return CreateSymbolCommand(DbSymbolRepositoryFactory.create())
