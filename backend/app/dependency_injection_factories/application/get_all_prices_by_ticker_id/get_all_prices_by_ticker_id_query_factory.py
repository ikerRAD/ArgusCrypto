from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query import (
    GetAllPricesByTickerIdQuery,
)
from app.dependency_injection_factories.infrastructure.crypto.database.repositories.db_price_repository_factory import (
    DbPriceRepositoryFactory,
)


class GetAllPricesByTickerIdQueryFactory:
    @staticmethod
    def create() -> GetAllPricesByTickerIdQuery:
        return GetAllPricesByTickerIdQuery(DbPriceRepositoryFactory.create())
