from app.infrastructure.crypto.repositories.db_price_repository import DbPriceRepository


class DbPriceRepositoryFactory:
    @staticmethod
    def create() -> DbPriceRepository:
        return DbPriceRepository()
