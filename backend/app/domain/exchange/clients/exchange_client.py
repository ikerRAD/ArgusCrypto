from abc import ABC, abstractmethod

from app.domain.crypto.models import Ticker, Price


class ExchangeClient(ABC):
    @abstractmethod
    def fetch_price_for_tickers(self, tickers: list[Ticker]) -> list[Price]:
        pass
