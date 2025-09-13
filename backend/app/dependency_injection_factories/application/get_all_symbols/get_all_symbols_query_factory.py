from app.application.get_all_symbols.get_all_symbols_query import GetAllSymbolsQuery
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_symbol_repository_factory import (
    DbSymbolRepositoryFactory,
)


class GetAllSymbolsQueryFactory:
    @staticmethod
    def create() -> GetAllSymbolsQuery:
        return GetAllSymbolsQuery(DbSymbolRepositoryFactory.create())
