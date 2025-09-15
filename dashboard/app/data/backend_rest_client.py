from typing import Type, TypeVar

import requests

from app.data.schemas.exchange import Exchange
from app.data.schemas.price import Price
from app.data.schemas.symbol import Symbol
from app.data.schemas.ticker import Ticker

T = TypeVar("T", bound=object)


class BackendRestClient:
    def __init__(self, base_url: str):
        self.__base_url = base_url

        self.__get_all_symbols_endpoint = "/v1/symbols"
        self.__get_all_exchanges_endpoint = "/v1/exchanges"
        self.__get_exchange_by_id_endpoint = "/v1/exchanges/{exchange_id}"
        self.__get_all_tickers_by_exchange_id_endpoint = (
            "/v1/exchanges/{exchange_id}/tickers"
        )
        self.__get_ticker_by_id_endpoint = "/v1/tickers/{ticker_id}"
        self.__get_all_prices_by_ticker_id_endpoint = "/v1/tickers/{ticker_id}/prices"

    def get_all_symbols(self) -> list[Symbol]:
        return self.__get_all_by_endpoint(self.__get_all_symbols_endpoint, Symbol)

    def get_all_exchanges(self) -> list[Exchange]:
        return self.__get_all_by_endpoint(self.__get_all_exchanges_endpoint, Exchange)

    def get_exchange_by_id(self, exchange_id: int) -> Exchange:
        return self.__get_one_by_endpoint(
            self.__get_exchange_by_id_endpoint.format(exchange_id=exchange_id), Exchange
        )

    def get_all_tickers_by_exchange_id(self, exchange_id: int) -> list[Ticker]:
        return self.__get_all_by_endpoint(
            self.__get_all_tickers_by_exchange_id_endpoint.format(
                exchange_id=exchange_id
            ),
            Ticker,
        )

    def get_ticker_by_id(self, ticker_id: int) -> Ticker:
        return self.__get_one_by_endpoint(
            self.__get_ticker_by_id_endpoint.format(ticker_id=ticker_id), Ticker
        )

    def get_all_prices_by_ticker_id(
        self, ticker_id: int, start_date: None | str = None, end_date: None | str = None
    ) -> list[Price]:
        endpoint = self.__get_all_prices_by_ticker_id_endpoint.format(
            ticker_id=ticker_id
        )

        if start_date is not None and end_date is not None:
            endpoint = f"{endpoint}?start_date={start_date}&end_date={end_date}"
        elif start_date is not None:
            endpoint = f"{endpoint}?start_date={start_date}"
        elif end_date is not None:
            endpoint = f"{endpoint}?end_date={end_date}"

        return self.__get_all_by_endpoint(endpoint, Price)

    def __get_one_by_endpoint(self, endpoint: str, dataclass_: Type[T]) -> T:
        response = requests.get(self.__base_url + endpoint)
        response.raise_for_status()

        return dataclass_(**response.json())

    def __get_all_by_endpoint(self, endpoint: str, dataclass_: Type[T]) -> list[T]:
        response = requests.get(self.__base_url + endpoint)
        response.raise_for_status()

        return [dataclass_(**class_dict) for class_dict in response.json()]
