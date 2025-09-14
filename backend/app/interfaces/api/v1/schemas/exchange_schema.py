from __future__ import annotations
from pydantic import BaseModel

from app.domain.exchange.models.exchange import Exchange


class ExchangeSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_domain(domain_exchange: Exchange) -> ExchangeSchema:
        return ExchangeSchema(id=domain_exchange.id, name=domain_exchange.name)
