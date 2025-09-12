from abc import ABC, abstractmethod

from app.domain.exchange.models import Exchange


class ExchangeRepository(ABC):
    @abstractmethod
    def find_exchange(self, fetch_tickers=False) -> Exchange:
        pass
