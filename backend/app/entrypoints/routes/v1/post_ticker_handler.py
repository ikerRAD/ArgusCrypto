from fastapi import HTTPException

from app.application.create_ticker.create_ticker_command import CreateTickerCommand
from app.dependency_injection_factories.application.create_ticker.create_ticker_command_factory import (
    CreateTickerCommandFactory,
)
from app.domain.crypto.exceptions.reference_to_non_existent_id_exception import (
    ReferenceToNonExistentIdException,
)
from app.domain.crypto.exceptions.ticker_already_exists_exception import (
    TickerAlreadyExistsException,
)
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.ticker_create_schema import TickerCreateSchema
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema
from app.main import logger


class PostTickerHandler(RouteHandler):
    def __init__(self, command: None | CreateTickerCommand = None):
        self.__command = command or CreateTickerCommandFactory.create()

    def handle(self, ticker_schema: TickerCreateSchema) -> TickerSchema:
        try:
            logger.info(
                f"Creating ticker '{ticker_schema.ticker}' for exchange "
                f"'{ticker_schema.exchange_id}' and symbol '{ticker_schema.symbol_id}'"
            )
            response = self.__command.execute(
                TickerCreateSchema.to_domain(ticker_schema)
            )

            return TickerSchema.from_domain(response.created_ticker)
        except TickerAlreadyExistsException:
            logger.error(
                f"Ticker '{ticker_schema.ticker}' already exists for exchange '{ticker_schema.exchange_id}'"
            )
            raise HTTPException(
                status_code=409,
                detail=f"Ticker '{ticker_schema.ticker}' already exists for exchange '{ticker_schema.exchange_id}'",
            )
        except ReferenceToNonExistentIdException as e:
            logger.error(
                f"symbol_id '{ticker_schema.symbol_id}' or exchange_id '{ticker_schema.exchange_id}' are non-existent: {e}"
            )
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(
                f"An unexpected error happened creating the ticker '{ticker_schema.ticker}' "
                f"for exchange '{ticker_schema.exchange_id}' and symbol '{ticker_schema.symbol_id}': {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")
