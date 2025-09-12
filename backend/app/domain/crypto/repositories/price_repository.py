from abc import ABC, abstractmethod

from app.domain.crypto.models import Price


class PriceRepository(ABC):
    @abstractmethod
    def bulk_save(self, prices: list[Price]) -> None:
        pass
