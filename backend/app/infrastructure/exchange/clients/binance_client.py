import json

import httpx

from app.domain.crypto.models.price import Price
from app.domain.crypto.models.ticker import Ticker
from app.domain.exchange.clients.exchange_client import ExchangeClient


class BinanceClient(ExchangeClient):
    __BINANCE_API_PRICE_PATH = "/api/v3/ticker/price"

    def __init__(self, api_base_url: str):
        self.__binance_api_url = api_base_url + self.__BINANCE_API_PRICE_PATH

    def fetch_price_for_tickers(self, tickers: list[Ticker]) -> list[Price]:
        if not tickers:
            return []

        ticker_map = self._map_tickers_by_symbol(tickers)
        prices: list[Price] = []

        with httpx.Client() as client:
            response = client.get(
                self.__binance_api_url, params=self.__get_params_from_tickers(tickers)
            )

            if response.status_code == 200:
                for item in response.json():
                    price = self.__map_json_to_price(item, ticker_map)
                    prices.append(price)

        return prices

    @staticmethod
    def __get_params_from_tickers(tickers: list[Ticker]) -> dict[str, str]:
        symbols = [ticker.ticker for ticker in tickers]
        return {"symbols": json.dumps(symbols, separators=(",", ":"))}

    @staticmethod
    def __map_json_to_price(
        price_json: dict[str, str], ticker_map: dict[str, Ticker]
    ) -> Price:
        ticker = ticker_map[price_json["symbol"]]

        return Price(ticker_id=ticker.id, price=float(price_json["price"]))
