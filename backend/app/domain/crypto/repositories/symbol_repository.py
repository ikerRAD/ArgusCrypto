from abc import ABC, abstractmethod

from app.domain.crypto.models.symbol import Symbol


class SymbolRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Symbol]:
        pass
