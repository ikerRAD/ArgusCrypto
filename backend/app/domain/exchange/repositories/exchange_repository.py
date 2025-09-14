from abc import ABC, abstractmethod

from app.domain.exchange.models.exchange import Exchange


class ExchangeRepository(ABC):
    @abstractmethod
    def get_or_fail_by_name(self, exchange_name: str, fetch_tickers: bool) -> Exchange:
        pass

    @abstractmethod
    def get_all(self) -> list[Exchange]:
        pass
