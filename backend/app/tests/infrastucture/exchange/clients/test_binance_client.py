from unittest import TestCase
from unittest.mock import patch, Mock

from httpx import Response, Client

from app.domain.crypto.models.ticker import Ticker
from app.infrastructure.exchange.clients.binance_client import BinanceClient


class TestBinanceClient(TestCase):
    def setUp(self) -> None:
        self.btcusdt_ticker = Ticker(id=1, ticker="BTCUSDT", symbol_id=1, exchange_id=1)
        self.btceur_ticker = Ticker(id=2, ticker="BTCEUR", symbol_id=2, exchange_id=1)

        self.client = BinanceClient("http://binance.example.test")

    @patch("app.infrastructure.exchange.clients.binance_client.httpx.Client")
    def test_fetch_price_for_tickers(self, httpx_client_class: Mock) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.json.return_value = [
            {"symbol": "BTCUSDT", "price": "100.000020"},
            {"symbol": "BTCEUR", "price": "200.0"},
        ]
        httpx_client = Mock(spec=Client)
        httpx_client.get.return_value = response
        httpx_client_class.return_value.__enter__.return_value = httpx_client

        result = self.client.fetch_price_for_tickers(
            [self.btcusdt_ticker, self.btceur_ticker]
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].ticker_id, self.btcusdt_ticker.id)
        self.assertEqual(result[0].price, 100.000020)
        self.assertEqual(result[1].ticker_id, self.btceur_ticker.id)
        self.assertEqual(result[1].price, 200.0)
        httpx_client.get.assert_called_once_with(
            "http://binance.example.test/api/v3/ticker/price",
            params={"symbols": '["BTCUSDT","BTCEUR"]'},
        )

    def test_fetch_price_for_empty_tickers(self) -> None:
        result = self.client.fetch_price_for_tickers([])

        self.assertEqual(result, [])

    @patch("app.infrastructure.exchange.clients.binance_client.httpx.Client")
    def test_fetch_price_for_tickers_request_fails(
        self, httpx_client_class: Mock
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 500
        httpx_client = Mock(spec=Client)
        httpx_client.get.return_value = response
        httpx_client_class.return_value.__enter__.return_value = httpx_client

        result = self.client.fetch_price_for_tickers(
            [self.btcusdt_ticker, self.btceur_ticker]
        )

        self.assertEqual(result, [])
        httpx_client.get.assert_called_once_with(
            "http://binance.example.test/api/v3/ticker/price",
            params={"symbols": '["BTCUSDT","BTCEUR"]'},
        )
