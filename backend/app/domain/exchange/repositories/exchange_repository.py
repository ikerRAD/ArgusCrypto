from abc import ABC, abstractmethod

from app.domain.exchange.models import Exchange


class ExchangeRepository(ABC):
    @abstractmethod
    def find_exchange(self, exchange_name: str, fetch_tickers: bool) -> Exchange:
        pass
