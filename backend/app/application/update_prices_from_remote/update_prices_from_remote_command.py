from app.application import Instruction, Response
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.domain.exchange.clients.exchange_client import ExchangeClient
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class UpdatePricesFromRemoteCommand(Instruction):
    def __init__(
        self,
        exchange_client: ExchangeClient,
        exchange_repository: ExchangeRepository,
        price_repository: PriceRepository,
    ):
        self.__exchange_client = exchange_client
        self.__exchange_repository = exchange_repository
        self.__price_repository = price_repository

    def execute(self) -> Response | None:
        exchange = self.__exchange_repository.find_exchange(fetch_tickers=True)

        fetched_prices = self.__exchange_client.fetch_price_for_tickers(
            exchange.tickers
        )

        self.__price_repository.bulk_save(fetched_prices)
