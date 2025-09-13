from abc import ABC, abstractmethod

from app.domain.exchange.models.exchange import Exchange


class ExchangeFinder(ABC):
    @abstractmethod
    def find(self, fetch_tickers=False) -> Exchange:
        pass
