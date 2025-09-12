from celery import Celery

from app.settings import CELERY_BROKER_URL, CELERY_BACKEND_URL, BINANCE_INTERVAL

celery_app = Celery(
    "crypto-tasks",
    broker=CELERY_BROKER_URL,  # Add your broker URL here
    backend=CELERY_BACKEND_URL,  # Add your backend URL here
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "fetch-binance-prices": {
        "task": "app.tasks.fetch_and_store_binance_cripto_prices",
        "schedule": BINANCE_INTERVAL,
    }
}


@celery_app.task
def fetch_and_store_binance_cripto_prices():
    from app.entrypoints.tasks.fetch_binance_prices_handler import (
        FetchBinancePricesHandler,
    )

    task_handler = FetchBinancePricesHandler()
    task_handler.handle()
