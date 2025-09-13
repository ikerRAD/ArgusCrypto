from app.domain.crypto.models.symbol import Symbol
from app.infrastructure.crypto.database.table_models import SymbolTableModel


class DbSymbolTranslator:
    def bulk_translate_to_domain_model(
        self, symbol_table_models: list[SymbolTableModel]
    ) -> list[Symbol]:
        return [
            self.translate_to_domain_model(symbol_table_model)
            for symbol_table_model in symbol_table_models
        ]

    def translate_to_domain_model(self, symbol_table_model: SymbolTableModel) -> Symbol:
        return Symbol(
            id=symbol_table_model.id,
            name=symbol_table_model.name,
            symbol=symbol_table_model.symbol,
        )
