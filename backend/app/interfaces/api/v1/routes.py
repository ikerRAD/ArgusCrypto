from datetime import datetime

from fastapi import APIRouter, status, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema
from app.interfaces.api.v1.schemas.price_schema import PriceSchema
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema
from app.interfaces.api.v1.schemas.ticker_create_schema import TickerCreateSchema
from app.interfaces.api.v1.schemas.ticker_schema import TickerSchema
from app.main import logger

router_v1 = APIRouter()


@router_v1.get("/symbols", response_model=list[SymbolSchema], tags=["Symbols"])
def get_all_symbols():
    from app.entrypoints.routes.v1.get_all_symbols_handler import GetAllSymbolsHandler

    handler = GetAllSymbolsHandler()
    return handler.handle()


@router_v1.get(
    "/symbols/{symbol_id}",
    response_model=SymbolSchema,
    responses={
        404: {
            "description": "Symbol not found",
            "content": {
                "application/json": {"example": {"detail": "Symbol not found"}}
            },
        }
    },
    tags=["Symbols"],
)
def get_symbol_by_id(symbol_id: int):
    from app.entrypoints.routes.v1.get_symbol_by_id_handler import GetSymbolByIdHandler

    handler = GetSymbolByIdHandler()
    return handler.handle(symbol_id)


@router_v1.post(
    "/symbols",
    status_code=status.HTTP_201_CREATED,
    response_model=SymbolSchema,
    responses={
        409: {
            "description": "Symbol already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Symbol 'SYMBOL' already exists"}
                }
            },
        }
    },
    tags=["Symbols"],
)
def post_symbol(symbol: SymbolCreateSchema):
    from app.entrypoints.routes.v1.post_symbol_handler import PostSymbolHandler

    handler = PostSymbolHandler()
    return handler.handle(symbol)


@router_v1.get("/exchanges", response_model=list[ExchangeSchema], tags=["Exchanges"])
def get_all_exchanges():
    from app.entrypoints.routes.v1.get_all_exchanges_handler import (
        GetAllExchangesHandler,
    )

    handler = GetAllExchangesHandler()
    return handler.handle()


@router_v1.get(
    "/exchanges/{exchange_id}",
    response_model=ExchangeSchema,
    responses={
        404: {
            "description": "Exchange not found",
            "content": {
                "application/json": {"example": {"detail": "Exchange not found"}}
            },
        }
    },
    tags=["Exchanges"],
)
def get_exchange_by_id(exchange_id: int):
    from app.entrypoints.routes.v1.get_exchange_by_id_handler import (
        GetExchangeByIdHandler,
    )

    handler = GetExchangeByIdHandler()
    return handler.handle(exchange_id)


@router_v1.get(
    "/exchanges/{exchange_id}/tickers",
    response_model=list[TickerSchema],
    responses={
        404: {
            "description": "Exchange not found",
            "content": {
                "application/json": {"example": {"detail": "Exchange not found"}}
            },
        }
    },
    tags=["Tickers"],
)
def get_all_tickers_by_exchange_id(exchange_id: int):
    from app.entrypoints.routes.v1.get_all_tickers_by_exchange_id_handler import (
        GetAllTickersByExchangeIdHandler,
    )

    handler = GetAllTickersByExchangeIdHandler()
    return handler.handle(exchange_id)


@router_v1.get(
    "/tickers/{ticker_id}",
    response_model=TickerSchema,
    responses={
        404: {
            "description": "Ticker not found",
            "content": {
                "application/json": {"example": {"detail": "Ticker not found"}}
            },
        }
    },
    tags=["Tickers"],
)
def get_ticker_by_id(ticker_id: int):
    from app.entrypoints.routes.v1.get_ticker_by_id_handler import GetTickerByIdHandler

    handler = GetTickerByIdHandler()
    return handler.handle(ticker_id)


@router_v1.post(
    "/tickers",
    status_code=status.HTTP_201_CREATED,
    response_model=TickerSchema,
    responses={
        409: {
            "description": "Ticker already exists for exchange",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ticker 'BTCUSD' already exists for exchange with id '1'"
                    }
                }
            },
        },
        400: {
            "description": "symbol_id or exchange_id are non-existent",
            "content": {
                "application/json": {
                    "example": {"detail": "symbol_id '0' is non-existent"}
                }
            },
        },
    },
    tags=["Tickers"],
)
def post_ticker(symbol: TickerCreateSchema):
    from app.entrypoints.routes.v1.post_ticker_handler import PostTickerHandler

    handler = PostTickerHandler()
    return handler.handle(symbol)


@router_v1.get(
    "/tickers/{ticker_id}/prices",
    response_model=list[PriceSchema],
    responses={
        400: {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {"detail": "start_date must be before end_date"}
                }
            },
        },
        404: {
            "description": "Ticker not found",
            "content": {
                "application/json": {"example": {"detail": "Ticker not found"}}
            },
        },
    },
    tags=["Prices"],
)
def get_all_prices_by_ticker_id(
    ticker_id: int, start_date: datetime | None = None, end_date: datetime | None = None
):
    from app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler import (
        GetAllPricesByTickerIdHandler,
    )

    handler = GetAllPricesByTickerIdHandler()
    return handler.handle(ticker_id, start_date, end_date)


@router_v1.websocket(
    "/tickers/{ticker_id}/prices/ws",
)
async def get_all_prices_by_ticker_id_ws(
    websocket: WebSocket, ticker_id: int, last_minutes: int = 10
):
    from app.entrypoints.routes.v1.get_all_prices_by_ticker_id_handler import (
        GetAllPricesByTickerIdHandler,
    )

    handler = GetAllPricesByTickerIdHandler()

    try:
        await websocket.accept()
        await handler.handle_websocket(websocket, ticker_id, last_minutes)

    except WebSocketDisconnect:
        logger.info(f"Websocket for ticker_id {ticker_id} disconnected")
    except Exception as e:
        logger.error(f"Websocket for ticker_id {ticker_id} failed: {e}")
        await websocket.close()
