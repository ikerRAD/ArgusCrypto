from fastapi import APIRouter

from app.interfaces.api.v1.schemas.symbol_create_schema import SymbolCreateSchema
from app.interfaces.api.v1.schemas.symbol_schema import SymbolSchema

router_v1 = APIRouter()


@router_v1.get("/symbols", response_model=list[SymbolSchema])
def get_all_symbols():
    from app.entrypoints.routes.v1.get_all_symbols_handler import GetAllSymbolsHandler

    handler = GetAllSymbolsHandler()
    return handler.handle()


@router_v1.get("/symbols/{symbol_id}", response_model=SymbolSchema)
def get_symbol_by_id(symbol_id: int):
    pass


@router_v1.post("/symbols", response_model=SymbolSchema)
def post_symbol(symbol: SymbolCreateSchema):
    pass
