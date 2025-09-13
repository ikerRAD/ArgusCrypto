from __future__ import annotations

from pydantic import BaseModel

from app.domain.crypto.models.symbol import Symbol


class SymbolCreateSchema(BaseModel):
    name: str
    symbol: str

    @staticmethod
    def to_domain(symbol_create_schema: SymbolCreateSchema) -> Symbol:
        return Symbol(
            name=symbol_create_schema.name, symbol=symbol_create_schema.symbol
        )
