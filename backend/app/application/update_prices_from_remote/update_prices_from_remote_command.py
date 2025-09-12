from app.application import Instruction
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.domain.exchange.clients.exchange_client import ExchangeClient
from app.domain.exchange.finders.exchange_finder import ExchangeFinder


class UpdatePricesFromRemoteCommand(Instruction):
    def __init__(
        self,
        exchange_client: ExchangeClient,
        exchange_finder: ExchangeFinder,
        price_repository: PriceRepository,
    ):
        self.__exchange_client = exchange_client
        self.__exchange_finder = exchange_finder
        self.__price_repository = price_repository

    def execute(self) -> None:
        exchange = self.__exchange_finder.find(fetch_tickers=True)

        fetched_prices = self.__exchange_client.fetch_price_for_tickers(
            exchange.tickers
        )

        self.__price_repository.bulk_save(fetched_prices)
