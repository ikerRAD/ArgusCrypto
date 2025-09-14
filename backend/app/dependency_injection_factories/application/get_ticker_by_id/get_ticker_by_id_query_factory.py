from app.application.get_ticker_by_id.get_ticker_by_id_query import GetTickerByIdQuery
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_ticker_repository_factory import \
    DbTickerRepositoryFactory


class GetTickerByIdQueryFactory:
    @staticmethod
    def create() -> GetTickerByIdQuery:
        return GetTickerByIdQuery(
            DbTickerRepositoryFactory.create()
        )