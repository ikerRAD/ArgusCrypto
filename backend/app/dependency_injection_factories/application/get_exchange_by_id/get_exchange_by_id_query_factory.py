from app.application.get_exchange_by_id.get_exchange_by_id_query import (
    GetExchangeByIdQuery,
)
from app.dependency_injection_factories.infrastructure.exchange.database.repositories.db_exchange_repository_factory import (
    DbExchangeRepositoryFactory,
)


class GetExchangeByIdQueryFactory:
    @staticmethod
    def create() -> GetExchangeByIdQuery:
        return GetExchangeByIdQuery(
            DbExchangeRepositoryFactory.create(),
        )
