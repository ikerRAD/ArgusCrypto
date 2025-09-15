from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.crypto.models.price import Price


class PriceRepository(ABC):
    @abstractmethod
    def bulk_save(self, prices: list[Price]) -> None:
        pass

    @abstractmethod
    def get_all_or_fail_by_ticker_id(
        self,
        ticker_id: int,
        start_date: None | datetime,
        end_date: None | datetime,
        include_end=True,
        check_ticker=True,
    ) -> list[Price]:
        pass
