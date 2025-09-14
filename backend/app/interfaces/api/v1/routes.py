from fastapi import APIRouter, status

from app.interfaces.api.v1.schemas.exchange_schema import ExchangeSchema
from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema

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
def get_exchange_by_id(schema_id: int):
    pass
