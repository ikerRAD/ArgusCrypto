from abc import ABC, abstractmethod

from app.domain.crypto.models import Ticker, Price


class ExchangeClient(ABC):
    @abstractmethod
    def fetch_price_for_tickers(self, tickers: list[Ticker]) -> list[Price]:
        pass

    @staticmethod
    def _map_tickers_by_symbol(tickers: list[Ticker]) -> dict[str, Ticker]:
        return {ticker.ticker: ticker for ticker in tickers}
