from celery import Celery
from celery.utils.log import get_task_logger

from app.settings import (
    CELERY_BROKER_URL,
    CELERY_BACKEND_URL,
    BINANCE_INTERVAL,
    KRAKEN_INTERVAL,
)

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
    },
    "fetch-kraken-prices": {
        "task": "app.tasks.fetch_and_store_kraken_cripto_prices",
        "schedule": KRAKEN_INTERVAL,
    },
}

logger = get_task_logger(__name__)


@celery_app.task
def fetch_and_store_binance_cripto_prices():
    from app.entrypoints.tasks.fetch_binance_prices_handler import (
        FetchBinancePricesHandler,
    )

    task_handler = FetchBinancePricesHandler()
    task_handler.handle()


@celery_app.task
def fetch_and_store_kraken_cripto_prices():
    from app.entrypoints.tasks.fetch_kraken_prices_handler import (
        FetchKrakenPricesHandler,
    )

    task_handler = FetchKrakenPricesHandler()
    task_handler.handle()
