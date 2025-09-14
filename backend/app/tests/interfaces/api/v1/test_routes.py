from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db import Base
from app.infrastructure.crypto.database.table_models import (
    SymbolTableModel,
    TickerTableModel,
)
from app.infrastructure.exchange.database.table_models import ExchangeTableModel
from app.main import app

import app.db as db


class TestRoutes(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        @event.listens_for(cls.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

        cls.TestingSessionLocal = sessionmaker(bind=cls.engine, expire_on_commit=False)
        Base.metadata.create_all(bind=cls.engine)

        cls.patcher_engine = patch.object(db, "engine", cls.engine)
        cls.patcher_session = patch.object(db, "SessionLocal", cls.TestingSessionLocal)

        cls.patcher_engine.start()
        cls.patcher_session.start()

        with cls.TestingSessionLocal() as session:
            session.add_all(
                [
                    SymbolTableModel(id=1, name="Bitcoin", symbol="BTC"),
                    SymbolTableModel(id=2, name="Ethereum", symbol="ETH"),
                    SymbolTableModel(id=3, name="Cardano", symbol="ADA"),
                ]
            )
            session.commit()

            session.add_all(
                [
                    ExchangeTableModel(id=1, name="Binance"),
                    ExchangeTableModel(id=2, name="Kraken"),
                ]
            )
            session.commit()

            session.add_all(
                [
                    TickerTableModel(
                        id=1, ticker="BTCUSDT", exchange_id=1, symbol_id=1
                    ),
                    TickerTableModel(id=2, ticker="BTCEUR", exchange_id=1, symbol_id=1),
                ]
            )
            session.commit()

        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.patcher_engine.stop()
        cls.patcher_session.stop()

    def test_get_all_symbols(self) -> None:
        expected_status_code = 200
        expected_content = [
            {"id": 1, "name": "Bitcoin", "symbol": "BTC"},
            {"id": 2, "name": "Ethereum", "symbol": "ETH"},
            {"id": 3, "name": "Cardano", "symbol": "ADA"},
        ]

        response = self.client.get("/v1/symbols")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_all_symbols.get_all_symbols_query_factory.GetAllSymbolsQueryFactory.create"
    )
    def test_get_all_symbols_fail(self, get_all_symbols_query_create: Mock) -> None:
        get_all_symbols_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/symbols")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_symbol_by_id(self) -> None:
        expected_status_code = 200
        expected_content = {"id": 1, "name": "Bitcoin", "symbol": "BTC"}

        response = self.client.get("/v1/symbols/1")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_symbol_by_id_invalid_id(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "symbol_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "1aq",
                }
            ]
        }

        response = self.client.get("/v1/symbols/1aq")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_symbol_by_id_not_found(self) -> None:
        expected_status_code = 404
        expected_content = {"detail": "Symbol not found"}

        response = self.client.get("/v1/symbols/8000")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_symbol_by_id.get_symbol_by_id_query_factory.GetSymbolByIdQueryFactory.create"
    )
    def test_get_symbol_by_id_fail(self, get_symbol_by_id_query_create: Mock) -> None:
        get_symbol_by_id_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/symbols/11")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_symbol(self) -> None:
        expected_status_code = 201
        expected_content = {"id": 4, "name": "Dogecoin", "symbol": "DOGE"}

        response = self.client.post(
            "/v1/symbols", content='{"name": "Dogecoin", "symbol": "DOGE"}'
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_symbol_conflict(self) -> None:
        expected_status_code = 409
        expected_content = {"detail": "Symbol 'ETH' already exists"}

        response = self.client.post(
            "/v1/symbols", content='{"name": "Ethereum", "symbol": "ETH"}'
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_symbol_validation_error(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "input": {"symbol": "ETH"},
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }

        response = self.client.post("/v1/symbols", content='{"symbol": "ETH"}')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.create_symbol.create_symbol_command_factory.CreateSymbolCommandFactory.create"
    )
    def test_post_symbol_fail(self, create_symbol_command_create: Mock) -> None:
        create_symbol_command_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.post(
            "/v1/symbols", content='{"name": "Shiva Inu", "symbol": "SHIV"}'
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_all_exchanges(self) -> None:
        expected_status_code = 200
        expected_content = [{"id": 1, "name": "Binance"}, {"id": 2, "name": "Kraken"}]

        response = self.client.get("/v1/exchanges")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_all_exchanges.get_all_exchanges_query_factory.GetAllExchangesQueryFactory.create"
    )
    def test_get_all_exchanges_fail(self, get_all_exchanges_query_create: Mock) -> None:
        get_all_exchanges_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/exchanges")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_exchange_by_id(self) -> None:
        expected_status_code = 200
        expected_content = {"id": 1, "name": "Binance"}

        response = self.client.get("/v1/exchanges/1")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_exchange_by_id_invalid_id(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "exchange_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "1aq",
                }
            ]
        }

        response = self.client.get("/v1/exchanges/1aq")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_exchanges_by_id_not_found(self) -> None:
        expected_status_code = 404
        expected_content = {"detail": "Exchange not found"}

        response = self.client.get("/v1/exchanges/8000")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_exchange_by_id.get_exchange_by_id_query_factory.GetExchangeByIdQueryFactory.create"
    )
    def test_get_exchanges_by_id_fail(
        self, get_exchange_by_id_query_create: Mock
    ) -> None:
        get_exchange_by_id_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/exchanges/11")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_tickers_by_exchange_id(self) -> None:
        expected_status_code = 200
        expected_content = [
            {"id": 1, "symbol_id": 1, "exchange_id": 1, "ticker": "BTCUSDT"},
            {"id": 2, "symbol_id": 1, "exchange_id": 1, "ticker": "BTCEUR"},
        ]

        response = self.client.get("/v1/exchanges/1/tickers")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertCountEqual(expected_content, response.json())

    def test_get_tickers_by_exchange_id_invalid_id(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "exchange_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "1aq",
                }
            ]
        }

        response = self.client.get("/v1/exchanges/1aq/tickers")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_tickers_by_exchanges_id_not_found(self) -> None:
        expected_status_code = 404
        expected_content = {"detail": "Exchange not found"}

        response = self.client.get("/v1/exchanges/8000/tickers")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_all_tickers_by_exchange_id.get_all_tickers_by_exchange_id_query_factory.GetAllTickersByExchangeIdQueryFactory.create"
    )
    def test_get_tickers_by_exchanges_id_fail(
        self, get_all_tickers_by_exchange_id_query: Mock
    ) -> None:
        get_all_tickers_by_exchange_id_query.return_value.execute.side_effect = (
            Exception()
        )
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/exchanges/11/tickers")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_ticker_by_id(self) -> None:
        expected_status_code = 200
        expected_content = {
            "id": 1,
            "symbol_id": 1,
            "exchange_id": 1,
            "ticker": "BTCUSDT",
        }

        response = self.client.get("/v1/tickers/1")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_ticker_by_id_invalid_id(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "ticker_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "1aq",
                }
            ]
        }

        response = self.client.get("/v1/tickers/1aq")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_get_ticker_by_id_not_found(self) -> None:
        expected_status_code = 404
        expected_content = {"detail": "Ticker not found"}

        response = self.client.get("/v1/tickers/8000")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.get_ticker_by_id.get_ticker_by_id_query_factory.GetTickerByIdQueryFactory.create"
    )
    def test_get_ticker_by_id_fail(self, get_ticker_by_id_query_create: Mock) -> None:
        get_ticker_by_id_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/tickers/11")

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_ticker(self) -> None:
        expected_status_code = 201
        expected_content = {
            "id": 3,
            "symbol_id": 1,
            "exchange_id": 1,
            "ticker": "BTC2USDT2",
        }

        response = self.client.post(
            "/v1/tickers",
            content='{"symbol_id": 1,"exchange_id": 1,"ticker": "BTC2USDT2"}',
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_ticker_conflict(self) -> None:
        expected_status_code = 409
        expected_content = {
            "detail": "Ticker 'BTCUSDT' already exists for exchange '1'"
        }

        response = self.client.post(
            "/v1/tickers",
            content='{"symbol_id": 1,"exchange_id": 1,"ticker": "BTCUSDT"}',
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    def test_post_ticker_symbol_id_not_exists(self) -> None:
        expected_status_code = 400
        expected_content = {"detail": "symbol_id '1000' is non-existent"}

        response = self.client.post(
            "/v1/tickers",
            content='{"symbol_id": 1000,"exchange_id": 1,"ticker": "BTCUSDT1"}',
        )

        self.assertEqual(expected_content, response.json())
        self.assertEqual(expected_status_code, response.status_code)

    def test_post_ticker_validation_error(self) -> None:
        expected_status_code = 422
        expected_content = {
            "detail": [
                {
                    "input": {"symbol_id": 1, "exchange_id": 1},
                    "loc": ["body", "ticker"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }

        response = self.client.post(
            "/v1/tickers", content='{"symbol_id": 1,"exchange_id": 1}'
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())

    @patch(
        "app.dependency_injection_factories.application.create_ticker.create_ticker_command_factory.CreateTickerCommandFactory.create"
    )
    def test_post_ticker_fail(self, create_ticker_command_create: Mock) -> None:
        create_ticker_command_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.post(
            "/v1/tickers",
            content='{"symbol_id": 1,"exchange_id": 1,"ticker": "BTC3USDT3"}',
        )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_content, response.json())
