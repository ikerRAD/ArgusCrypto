from abc import ABC, abstractmethod

from app.domain.crypto.models.symbol import Symbol


class SymbolRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Symbol]:
        pass

    @abstractmethod
    def get_or_fail_by_id(self, symbol_id: int) -> Symbol:
        pass

    @abstractmethod
    def insert(self, symbol: Symbol) -> Symbol:
        pass
