from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=308)
