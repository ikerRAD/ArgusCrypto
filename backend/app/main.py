from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.interfaces.api.v1.routes import router_v1

app = FastAPI(title="Argus Crypto API", version="1.0.0")

app.include_router(router_v1, prefix="/v1", tags=["v1"])


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=308)
