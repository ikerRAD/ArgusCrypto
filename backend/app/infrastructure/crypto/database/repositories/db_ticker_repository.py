from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.domain.crypto.exceptions.reference_to_non_existent_id_exception import (
    ReferenceToNonExistentIdException,
)
from app.domain.crypto.exceptions.ticker_already_exists_exception import (
    TickerAlreadyExistsException,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.ticker import Ticker
from app.domain.crypto.repositories.ticker_repository import TickerRepository
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.infrastructure.crypto.database.table_models import TickerTableModel
from app.infrastructure.crypto.database.translators.db_ticker_translator import (
    DbTickerTranslator,
)
from app.infrastructure.exchange.database.table_models import ExchangeTableModel


class DbTickerRepository(TickerRepository):
    def __init__(self, db_ticker_translator: DbTickerTranslator):
        self.__db_ticker_translator = db_ticker_translator

    def get_all_or_fail_by_exchange_id(self, exchange_id: int) -> list[Ticker]:
        with get_session() as session:
            query_result = session.execute(
                select(ExchangeTableModel).where(ExchangeTableModel.id == exchange_id)
            )
            exchange_table_model = query_result.scalar_one_or_none()

            if exchange_table_model is None:
                raise ExchangeNotFoundException("id", exchange_id)

            ticker_table_models = exchange_table_model.tickers

        return self.__db_ticker_translator.bulk_translate_to_domain_model(
            ticker_table_models
        )

    def get_or_fail_by_id(self, ticker_id: int) -> Ticker:
        with get_session() as session:
            query_result = session.execute(
                select(TickerTableModel).where(TickerTableModel.id == ticker_id)
            )
            ticker_table_model = query_result.scalar_one_or_none()

            if ticker_table_model is None:
                raise TickerNotFoundException(ticker_id)

        return self.__db_ticker_translator.translate_to_domain_model(ticker_table_model)

    def insert(self, ticker) -> Ticker:
        try:
            with get_session() as session:
                symbol_table_model = (
                    self.__db_ticker_translator.translate_to_table_model(ticker)
                )

                session.add(symbol_table_model)

            return self.__db_ticker_translator.translate_to_domain_model(
                symbol_table_model
            )

        except IntegrityError as e:
            msg = str(e.orig)
            if "unique_exchange_ticker" in msg or "UNIQUE" in msg:
                raise TickerAlreadyExistsException(ticker.ticker, ticker.exchange_id)
            else:
                attr: str
                attr_id: int
                if "exchange_id" in msg:
                    attr = "exchange_id"
                    attr_id = ticker.exchange_id
                else:
                    attr = "symbol_id"
                    attr_id = ticker.symbol_id

                raise ReferenceToNonExistentIdException(attr, attr_id)
