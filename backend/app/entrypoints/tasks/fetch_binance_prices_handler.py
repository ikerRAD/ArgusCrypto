from httpx import ConnectTimeout

from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.dependency_injection_factories.application.update_prices_from_remote.update_pricess_from_remote_command_factory import (
    UpdatePricesFromRemoteCommandFactory,
)
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.entrypoints.tasks import TaskHandler
from app.tasks import logger


class FetchBinancePricesHandler(TaskHandler):
    def __init__(self, command: None | UpdatePricesFromRemoteCommand = None):
        self.__command = (
            command or UpdatePricesFromRemoteCommandFactory.create_for_binance()
        )

    def handle(self) -> None:
        try:
            logger.info("Fetching Binance prices...")
            self.__command.execute()
        except ExchangeNotFoundException as e:
            logger.error(f"Binance is not a registered exchange: {e}")
        except ConnectTimeout:
            logger.error("The connection to Binance API has timed out")
        except Exception as e:
            logger.error(
                f"An unexpected error happened while fetching Binance prices: {e}"
            )
