from app.domain.exchange.finders.exchange_finder import ExchangeFinder
from app.domain.exchange.models.exchange import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class KrakenExchangeFinder(ExchangeFinder):
    __KRAKEN_EXCHANGE_NAME = "Kraken"

    def __init__(self, exchange_repository: ExchangeRepository):
        self.exchange_repository = exchange_repository

    def find(self, fetch_tickers=False) -> Exchange:
        return self.exchange_repository.find_exchange(
            self.__KRAKEN_EXCHANGE_NAME, fetch_tickers
        )
