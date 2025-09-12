from app.infrastructure.exchange.repositories.db_binance_repository import (
    DbBinanceRepository,
)


class DbBinanceRepositoryFactory:
    @staticmethod
    def create() -> DbBinanceRepository:
        return DbBinanceRepository()
