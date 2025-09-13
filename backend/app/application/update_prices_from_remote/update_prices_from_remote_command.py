from app.application import Instruction
from app.domain.crypto.repositories.price_repository import PriceRepository
from app.domain.exchange.clients.exchange_client import ExchangeClient
from app.domain.exchange.finders.exchange_finder import ExchangeFinder
from app.tasks import logger


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
        logger.error("COMMAND CALLED")
        exchange = self.__exchange_finder.find(fetch_tickers=True)

        logger.error(f"RETRIEVED EXCHANGE {exchange}")
        fetched_prices = self.__exchange_client.fetch_price_for_tickers(
            exchange.tickers
        )
        logger.error(f"RETRIEVED PRICES {fetched_prices}")

        self.__price_repository.bulk_save(fetched_prices)
