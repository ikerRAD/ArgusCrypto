from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models.exchange import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository
from app.infrastructure.exchange.database.table_models import ExchangeTableModel
from app.infrastructure.exchange.database.translators.db_exchange_translator import (
    DbExchangeTranslator,
)
from app.tasks import logger


class DbExchangeRepository(ExchangeRepository):
    def __init__(self, db_exchange_translator: DbExchangeTranslator):
        self.__db_exchange_translator = db_exchange_translator

    def find_exchange(self, exchange_name: str, fetch_tickers: bool) -> Exchange:
        with get_session() as session:
            statement = select(ExchangeTableModel).where(
                ExchangeTableModel.name == exchange_name
            )

            if fetch_tickers:
                statement = statement.options(selectinload(ExchangeTableModel.tickers))

            query_result = session.execute(statement)
            exchange_table_model: ExchangeTableModel | None = (
                query_result.scalar_one_or_none()
            )

            if exchange_table_model is None:
                raise ExchangeNotFoundException(exchange_name)

        return self.__db_exchange_translator.translate_to_domain_model(
            exchange_table_model, fetch_tickers
        )
