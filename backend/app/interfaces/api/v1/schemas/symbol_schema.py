from __future__ import annotations
from pydantic import BaseModel

from app.domain.crypto.models.symbol import Symbol


class SymbolSchema(BaseModel):
    id: int
    name: str
    symbol: str

    @staticmethod
    def from_domain(domain_symbol: Symbol) -> SymbolSchema:
        return SymbolSchema(
            id=domain_symbol.id,
            name=domain_symbol.name,
            symbol=domain_symbol.symbol,
        )
