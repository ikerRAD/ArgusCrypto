from abc import ABC, abstractmethod

from app.domain.crypto.models.ticker import Ticker


class TickerRepository(ABC):
    @abstractmethod
    def get_all_or_fail_by_exchange_id(self, exchange_id: int) -> list[Ticker]:
        pass

    @abstractmethod
    def get_or_fail_by_id(self, ticker_id: int) -> Ticker:
        pass