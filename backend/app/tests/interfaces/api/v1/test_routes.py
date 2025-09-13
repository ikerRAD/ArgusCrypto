from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db import Base
from app.infrastructure.crypto.database.table_models import SymbolTableModel
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
                    SymbolTableModel(id=3, name="Cardano", symbol="ADA"),
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
