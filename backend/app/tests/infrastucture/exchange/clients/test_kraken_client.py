from unittest import TestCase
from unittest.mock import patch, Mock

from httpx import Response, Client

from app.domain.crypto.models.ticker import Ticker
from app.infrastructure.exchange.clients.kraken_client import KrakenClient


class TestKrakenClient(TestCase):
    def setUp(self) -> None:
        self.xbtusdt_ticker = Ticker(id=3, ticker="XBTUSDT", symbol_id=1, exchange_id=2)
        self.xxbtzeur_ticker = Ticker(
            id=4, ticker="XXBTZEUR", symbol_id=2, exchange_id=2
        )

        self.client = KrakenClient("http://kraken.example.test")

    @patch("app.infrastructure.exchange.clients.kraken_client.httpx.Client")
    def test_fetch_price_for_tickers(self, httpx_client_class: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = {
            "error": [],
            "result": {
                "XBTUSDT": {
                    "a": ["10.000020", "1", "1.000"],
                    "b": ["98380.60000", "1", "1.000"],
                    "c": ["98380.70000", "0.00000508"],
                    "v": ["292.89615737", "454.15845172"],
                    "p": ["98355.07045", "98199.19375"],
                    "t": [22551, 29751],
                    "l": ["97965.30000", "97292.30000"],
                    "h": ["99087.00000", "99087.00000"],
                    "o": "98392.00000",
                },
                "XXBTZEUR": {
                    "a": ["2.0", "1", "1.000"],
                    "b": ["98380.60000", "1", "1.000"],
                    "c": ["98380.70000", "0.00000508"],
                    "v": ["292.89615737", "454.15845172"],
                    "p": ["98355.07045", "98199.19375"],
                    "t": [22551, 29751],
                    "l": ["97965.30000", "97292.30000"],
                    "h": ["99087.00000", "99087.00000"],
                    "o": "98392.00000",
                },
            },
        }
        httpx_client = Mock(spec=Client)
        httpx_client.get.return_value = response
        httpx_client_class.return_value.__enter__.return_value = httpx_client

        result = self.client.fetch_price_for_tickers(
            [self.xbtusdt_ticker, self.xxbtzeur_ticker]
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].ticker_id, self.xbtusdt_ticker.id)
        self.assertEqual(result[0].price, 10.000020)
        self.assertEqual(result[1].ticker_id, self.xxbtzeur_ticker.id)
        self.assertEqual(result[1].price, 2.0)
        httpx_client.get.assert_called_once_with(
            "http://kraken.example.test/0/public/Ticker",
            params={"pair": "XBTUSDT,XXBTZEUR"},
        )

    def test_fetch_price_for_empty_tickers(self) -> None:
        result = self.client.fetch_price_for_tickers([])

        self.assertEqual(result, [])

    @patch("app.infrastructure.exchange.clients.kraken_client.httpx.Client")
    def test_fetch_price_for_tickers_request_fails(
        self, httpx_client_class: Mock
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 500
        httpx_client = Mock(spec=Client)
        httpx_client.get.return_value = response
        httpx_client_class.return_value.__enter__.return_value = httpx_client

        result = self.client.fetch_price_for_tickers(
            [self.xbtusdt_ticker, self.xxbtzeur_ticker]
        )

        self.assertEqual(result, [])
        httpx_client.get.assert_called_once_with(
            "http://kraken.example.test/0/public/Ticker",
            params={"pair": "XBTUSDT,XXBTZEUR"},
        )
