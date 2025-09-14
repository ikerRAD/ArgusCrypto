from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db import Base
from app.infrastructure.crypto.database.table_models import SymbolTableModel
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
                    SymbolTableModel(id=3, name="Cardano", symbol="ADA")
                ]
            )
            session.commit()

            session.add_all(
                [
                    ExchangeTableModel(id=1, name="Binance"),
                    ExchangeTableModel(id=2, name="Kraken")
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
    def test_create_symbol_fail(self, create_symbol_command_create: Mock) -> None:
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
        expected_content = [
            {"id": 1, "name": "Binance"},
            {"id": 2, "name": "Kraken"}
        ]

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
