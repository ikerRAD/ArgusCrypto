from datetime import datetime

from sqlalchemy import select

from app.db import get_session
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.price import Price
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.infrastructure.crypto.database.table_models import (
    PriceTableModel,
    TickerTableModel,
)
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

    def get_all_or_fail_by_ticker_id(
        self,
        ticker_id: int,
        start_date: None | datetime,
        end_date: None | datetime,
        include_end=True,
        check_ticker=True,
    ) -> list[Price]:
        with get_session() as session:
            if check_ticker:
                ticker_check_query_result = session.execute(
                    select(TickerTableModel).where(TickerTableModel.id == ticker_id)
                )
                if ticker_check_query_result.scalar_one_or_none() is None:
                    raise TickerNotFoundException(ticker_id)

            statement = select(PriceTableModel).where(
                PriceTableModel.ticker_id == ticker_id
            )

            if start_date is not None:
                statement = statement.where(PriceTableModel.timestamp >= start_date)

            if end_date is not None:
                if include_end:
                    statement = statement.where(PriceTableModel.timestamp <= end_date)
                else:
                    statement = statement.where(PriceTableModel.timestamp < end_date)

            query_result = session.execute(
                statement.order_by(PriceTableModel.timestamp.asc())
            )

            price_table_models = query_result.scalars().all()

        return self.__db_price_translator.bulk_translate_to_domain_model(
            price_table_models
        )
