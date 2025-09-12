from typing import Any

import httpx

from app.domain.crypto.models import Ticker, Price
from app.domain.exchange.clients.exchange_client import ExchangeClient


class KrakenClient(ExchangeClient):
    __KRAKEN_API_PRICE_PATH = "/0/public/Ticker"

    def __init__(self, api_base_url: str):
        self.__kraken_api_url = api_base_url + self.__KRAKEN_API_PRICE_PATH

    def fetch_price_for_tickers(self, tickers: list[Ticker]) -> list[Price]:
        if not tickers:
            return []

        ticker_map = self._map_tickers_by_symbol(tickers)
        prices: list[Price] = []

        with httpx.Client() as client:
            response = client.get(
                self.__kraken_api_url, params=self.__get_params_from_tickers(tickers)
            )

            if response.status_code == 200:
                response_dict: dict[str, Any] = response.json()
                result_ticker_info = response_dict.get("result", {})
                for ticker in result_ticker_info:
                    prices.append(
                        Price(
                            ticker=ticker_map[ticker],
                            price=float(result_ticker_info[ticker]["a"][0]),
                        )
                    )

        return prices

    @staticmethod
    def __get_params_from_tickers(tickers: list[Ticker]) -> dict[str, str]:
        pairs = [ticker.ticker for ticker in tickers]
        return {"pair": ",".join(pairs)}
