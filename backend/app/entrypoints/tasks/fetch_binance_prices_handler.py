from app.application.update_prices_from_remote.update_prices_from_remote_command import (
    UpdatePricesFromRemoteCommand,
)
from app.dependency_injection_factories.application.update_prices_from_remote.update_pricess_from_remote_command_factory import (
    UpdatePricesFromRemoteCommandFactory,
)
from app.entrypoints.tasks import TaskHandler


class FetchBinancePricesHandler(TaskHandler):
    def __init__(self, command: None | UpdatePricesFromRemoteCommand = None):
        self.__command = (
            command or UpdatePricesFromRemoteCommandFactory.create_for_binance()
        )

    def handle(self) -> None:
        self.__command.execute()
