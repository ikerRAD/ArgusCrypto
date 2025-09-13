from app.db import get_session
from app.domain.crypto.models.price import Price
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.infrastructure.crypto.database.translators.db_price_translator import (
    DbPriceTranslator,
)


class DbPriceRepository(PriceRepository):
    def __init__(self, db_price_translator: DbPriceTranslator):
        self.__db_price_translator = db_price_translator

    def bulk_save(self, prices: list[Price]) -> None:
        with get_session() as session:
            session.add_all(
                self.__db_price_translator.bulk_translate_to_table_model(prices)
            )
