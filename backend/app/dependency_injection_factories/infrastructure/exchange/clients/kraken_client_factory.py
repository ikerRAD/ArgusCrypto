from app.infrastructure.exchange.clients.kraken_client import KrakenClient
from app.settings import KRAKEN_API_URL


class KrakenClientFactory:
    @staticmethod
    def create() -> KrakenClient:
        return KrakenClient(KRAKEN_API_URL)
