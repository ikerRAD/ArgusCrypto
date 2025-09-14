import logging
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("ArgusCryptoLogger")

app = FastAPI(title="Argus Crypto API", version="1.0.0")


from app.interfaces.api.v1.routes import router_v1
app.include_router(router_v1, prefix="/v1")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    app.openapi_schema = get_openapi(title="Argus Crypto API", version="1.0.0", routes=app.routes)

    app.openapi_schema["paths"]["/v1/tickers/{ticker_id}/prices/ws"] = {
        "get": {
            "tags": ["Prices"],
            "summary": "Real-time Prices By Ticker Id - last 10 minutes by default",
            "operationId": "get_all_prices_by_ticker_id_ws_v1_tickers__ticker_id__prices_ws",
            "parameters": [
                {
                    "name": "ticker_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer", "title": "Ticker Id"},
                },
                {
                    "name": "last_minutes",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "anyOf": [
                            {"type": "integer"},
                            {"type": "null"},
                        ],
                        "title": "Last minutes of data",
                    },
                },
            ]
        }
    }
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=308)
