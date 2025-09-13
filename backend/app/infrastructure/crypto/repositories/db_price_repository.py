from app.db import get_session
from app.domain.crypto.models.price import Price
from app.domain.crypto.repositories.price_repository import PriceRepository


class DbPriceRepository(PriceRepository):
    def bulk_save(self, prices: list[Price]) -> None:
        with get_session() as session:
            session.add_all(prices)
