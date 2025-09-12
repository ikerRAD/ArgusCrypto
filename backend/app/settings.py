import os

BINANCE_API_URL = os.getenv("BINANCE_API_BASE_URL", "https://api.binance.com")
KRAKEN_API_URL = os.getenv("KRAKEN_API_BASE_URL", "https://api.kraken.com")

CELERY_BROKER_USER = os.getenv("CELERY_BROKER_USER", "celery")
CELERY_BROKER_PASSWORD = os.getenv("CELERY_BROKER_PASSWORD", "celery")
CELERY_BROKER_HOST = os.getenv("CELERY_BROKER_HOST", "rabbitmq")
CELERY_BROKER_PORT = os.getenv("CELERY_BROKER_PORT", "5672")
CELERY_BROKER_VHOST = os.getenv("CELERY_BROKER_VHOST", "/")
CELERY_BROKER_URL = f"amqp://{CELERY_BROKER_USER}:{CELERY_BROKER_PASSWORD}@{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/{CELERY_BROKER_VHOST}"

CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "rpc://")

BINANCE_INTERVAL = min(float(os.getenv("BINANCE_INTERVAL", 10.0)), 10.0)
KRAKEN_INTERVAL = min(float(os.getenv("KRAKEN_INTERVAL", 10.0)), 10.0)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://database:database@db:5432/database"
)
