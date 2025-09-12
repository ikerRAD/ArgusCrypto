from app.infrastructure.exchange.clients.binance_client import BinanceClient
from app.settings import BINANCE_API_URL


class BinanceClientFactory:
    @staticmethod
    def create() -> BinanceClient:
        return BinanceClient(BINANCE_API_URL)
