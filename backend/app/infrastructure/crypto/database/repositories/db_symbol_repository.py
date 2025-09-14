from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.domain.crypto.exceptions.symbol_already_exists_exception import (
    SymbolAlreadyExistsException,
)
from app.domain.crypto.exceptions.symbol_not_found_exception import (
    SymbolNotFoundException,
)
from app.domain.crypto.models.symbol import Symbol
from app.domain.crypto.repositories.symbol_repository import SymbolRepository
from app.infrastructure.crypto.database.table_models import SymbolTableModel
from app.infrastructure.crypto.database.translators.db_symbol_translator import (
    DbSymbolTranslator,
)


class DbSymbolRepository(SymbolRepository):
    def __init__(self, db_symbol_translator: DbSymbolTranslator):
        self.__db_symbol_translator = db_symbol_translator

    def get_all(self) -> list[Symbol]:
        with get_session() as session:
            query_result = session.execute(select(SymbolTableModel))

            symbol_table_models = query_result.scalars().all()

        return self.__db_symbol_translator.bulk_translate_to_domain_model(
            symbol_table_models
        )

    def get_or_fail_by_id(self, symbol_id: int) -> Symbol:
        with get_session() as session:
            query_result = session.execute(
                select(SymbolTableModel).where(SymbolTableModel.id == symbol_id)
            )

            symbol_table_model = query_result.scalar_one_or_none()

            if symbol_table_model is None:
                raise SymbolNotFoundException(symbol_id)

        return self.__db_symbol_translator.translate_to_domain_model(symbol_table_model)

    def insert(self, symbol: Symbol) -> Symbol:
        try:
            with get_session() as session:
                symbol_table_model = (
                    self.__db_symbol_translator.translate_to_table_model(symbol)
                )

                session.add(symbol_table_model)

            return self.__db_symbol_translator.translate_to_domain_model(
                symbol_table_model
            )

        except IntegrityError:
            raise SymbolAlreadyExistsException(symbol.symbol)
