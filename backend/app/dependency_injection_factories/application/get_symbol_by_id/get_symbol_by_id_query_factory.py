from app.application.get_symbol_by_id.get_symbol_by_id_query import GetSymbolByIdQuery
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_symbol_repository_factory import (
    DbSymbolRepositoryFactory,
)


class GetSymbolByIdQueryFactory:
    @staticmethod
    def create() -> GetSymbolByIdQuery:
        return GetSymbolByIdQuery(DbSymbolRepositoryFactory.create())
