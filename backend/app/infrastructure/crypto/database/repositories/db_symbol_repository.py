from sqlalchemy import select

from app.db import get_session
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
