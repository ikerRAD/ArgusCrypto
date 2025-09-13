from app.infrastructure.exchange.database.repositories.db_exchange_repository import (
    DbExchangeRepository,
)


class DbExchangeRepositoryFactory:
    @staticmethod
    def create() -> DbExchangeRepository:
        return DbExchangeRepository()
