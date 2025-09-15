import asyncio
from datetime import datetime, timedelta

from fastapi import HTTPException, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query import (
    GetAllPricesByTickerIdQuery,
)
from app.dependency_injection_factories.application.get_all_prices_by_ticker_id.get_all_prices_by_ticker_id_query_factory import (
    GetAllPricesByTickerIdQueryFactory,
)
from app.domain.crypto.exceptions.ticker_not_found_exception import (
    TickerNotFoundException,
)
from app.domain.crypto.models.price import Price
from app.entrypoints.routes import RouteHandler
from app.interfaces.api.v1.schemas.price_schema import PriceSchema
from app.main import logger
from app.settings import PRICE_WEBSOCKET_INTERVAL


class GetAllPricesByTickerIdHandler(RouteHandler):
    def __init__(
        self,
        query: None | GetAllPricesByTickerIdQuery = None,
        websocket_interval: None | float = None,
    ):
        self.__query = query or GetAllPricesByTickerIdQueryFactory.create()
        self.__websocket_interval = websocket_interval or PRICE_WEBSOCKET_INTERVAL

    def handle(
        self, ticker_id: int, start_date: None | datetime, end_date: None | datetime
    ) -> list[PriceSchema]:
        if start_date is not None and end_date is not None and start_date > end_date:
            logger.error(
                f"Invalid date range [{start_date}, {end_date}] for querying prices for ticker '{ticker_id}'"
            )
            raise HTTPException(
                status_code=400, detail="start_date must be before end_date"
            )

        try:
            logger.info(
                f"Getting prices for ticker '{ticker_id}' in date range [{start_date}, {end_date}]"
            )
            response = self.__query.execute(ticker_id, start_date, end_date)

            return [PriceSchema.from_domain(price) for price in response.prices]
        except TickerNotFoundException:
            logger.error(f"Ticker with id '{ticker_id}' not found")
            raise HTTPException(status_code=404, detail="Ticker not found")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while retrieving prices for ticker with id '{ticker_id}' in date range [{start_date}, {end_date}]: {e}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error happened.")

    async def handle_websocket(
        self, websocket: WebSocket, ticker_id: int, last_minutes: int
    ):
        try:
            instant = datetime.now()
            response = self.__query.execute(
                ticker_id, instant - timedelta(minutes=last_minutes), instant, False
            )

            await self.__flush_prices(websocket, response.prices)

            previous_instant = instant
            while True:
                next_instant = datetime.now()

                response = self.__query.execute(
                    ticker_id, previous_instant, next_instant, False, False
                )
                await self.__flush_prices(websocket, response.prices)

                previous_instant = next_instant
                await asyncio.sleep(self.__websocket_interval)
        except TickerNotFoundException:
            logger.error(f"Ticker with id '{ticker_id}' not found")
            await websocket.send_json({"error": "Ticker not found"})
            raise
        except WebSocketDisconnect:
            raise
        except Exception as e:
            logger.error(f"An unexpected error happened in price websocket: {e}")
            await websocket.send_json({"error": "An unexpected error happened"})
            raise

    async def __flush_prices(self, websocket: WebSocket, prices: list[Price]) -> None:
        for price in prices:
            price_schema = PriceSchema.from_domain(price)
            await websocket.send_json(
                {
                    "id": price_schema.id,
                    "ticker_id": price_schema.ticker_id,
                    "price": price_schema.price,
                    "timestamp": price_schema.timestamp.isoformat(),
                }
            )
