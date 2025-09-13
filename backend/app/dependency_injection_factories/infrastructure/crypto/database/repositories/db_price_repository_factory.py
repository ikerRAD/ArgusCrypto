from app.infrastructure.crypto.database.repositories.db_price_repository import DbPriceRepository


class DbPriceRepositoryFactory:
    @staticmethod
    def create() -> DbPriceRepository:
        return DbPriceRepository()
