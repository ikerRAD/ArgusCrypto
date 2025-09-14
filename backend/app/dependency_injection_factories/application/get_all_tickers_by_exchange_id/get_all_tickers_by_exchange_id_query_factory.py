from app.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query import \
    GetAllTickersByExchangeIdQuery
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_ticker_repository_factory import \
    DbTickerRepositoryFactory


class GetAllTickersByExchangeIdQueryFactory:
    @staticmethod
    def create() -> GetAllTickersByExchangeIdQuery:
        return GetAllTickersByExchangeIdQuery(
            DbTickerRepositoryFactory.create()
        )