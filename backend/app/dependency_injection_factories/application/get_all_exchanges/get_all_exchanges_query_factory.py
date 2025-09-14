from app.application.get_all_exchanges.get_all_exchanges_query import (
    GetAllExchangesQuery,
)
from app.dependency_injection_factories.infrastructure.exchange.database.repositories.db_exchange_repository_factory import (
    DbExchangeRepositoryFactory,
)


class GetAllExchangesQueryFactory:
    @staticmethod
    def create() -> GetAllExchangesQuery:
        return GetAllExchangesQuery(DbExchangeRepositoryFactory.create())
