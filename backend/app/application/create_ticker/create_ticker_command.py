from app.application import Instruction
from app.application.create_ticker.create_ticker_command_response import (
    CreateTickerCommandResponse,
)
from app.domain.crypto.models.ticker import Ticker
from app.domain.crypto.repositories.ticker_repository import TickerRepository


class CreateTickerCommand(Instruction):
    def __init__(self, ticker_repository: TickerRepository):
        self.__ticker_repository = ticker_repository

    def execute(self, ticker: Ticker) -> CreateTickerCommandResponse:
        return CreateTickerCommandResponse(
            created_ticker=self.__ticker_repository.insert(ticker)
        )
