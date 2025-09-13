from contextlib import contextmanager
from typing import Generator
from unittest import TestCase
from unittest.mock import patch, Mock

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from app.db import Base
from app.infrastructure.crypto.database.table_models import SymbolTableModel
from app.main import app


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

        with cls.TestingSessionLocal() as session:
            session.add_all(
                [
                    SymbolTableModel(id=1, name="Bitcoin", symbol="BTC"),
                    SymbolTableModel(id=2, name="Ethereum", symbol="ETH"),
                    SymbolTableModel(id=3, name="Cardano", symbol="ADA"),
                ]
            )
            session.commit()

    def setUp(self) -> None:
        self.patcher = patch("app.db.get_session", new=self.get_test_session)
        self.patcher.start()

        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.patcher.stop()

    @classmethod
    @contextmanager
    def get_test_session(cls) -> Generator[Session, None, None]:
        session = cls.TestingSessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def test_get_all_symbols(self) -> None:
        expected_status_code = 200
        expected_content = [
            {"id": 1, "name": "Bitcoin", "symbol": "BTC"},
            {"id": 2, "name": "Ethereum", "symbol": "ETH"},
            {"id": 3, "name": "Cardano", "symbol": "ADA"},
        ]

        response = self.client.get("/v1/symbols")

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_content)

    @patch(
        "app.dependency_injection_factories.application.get_all_symbols.get_all_symbols_query_factory.GetAllSymbolsQueryFactory.create"
    )
    def test_get_all_symbols_fail(self, get_all_symbols_query_create: Mock) -> None:
        get_all_symbols_query_create.return_value.execute.side_effect = Exception()
        expected_status_code = 500
        expected_content = {"detail": "An unexpected error happened."}

        response = self.client.get("/v1/symbols")

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_content)
