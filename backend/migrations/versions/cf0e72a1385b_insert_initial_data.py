"""insert initial data

Revision ID: cf0e72a1385b
Revises: 35d554d2d18c
Create Date: 2025-09-11 16:22:43.995557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf0e72a1385b"
down_revision: Union[str, Sequence[str], None] = "35d554d2d18c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "symbols",
            sa.column("name", sa.String),
            sa.column("symbol", sa.String),
        ),
        [
            {"name": "Bitcoin", "symbol": "BTC"},
        ],
    )

    op.bulk_insert(
        sa.table(
            "exchanges",
            sa.column("name", sa.String),
        ),
        [
            {"name": "Binance"},
        ],
    )

    connection = op.get_bind()
    btc_symbol_id = connection.execute(
        sa.text("SELECT id FROM symbols WHERE symbol='BTC'")
    ).scalar_one()
    binance_exchange_id = connection.execute(
        sa.text("SELECT id FROM exchanges WHERE name='Binance'")
    ).scalar_one()

    op.bulk_insert(
        sa.table(
            "tickers",
            sa.column("symbol_id", sa.Integer),
            sa.column("exchange_id", sa.Integer),
            sa.column("ticker", sa.String),
        ),
        [
            {
                "symbol_id": btc_symbol_id,
                "exchange_id": binance_exchange_id,
                "ticker": "BTCUSDT",
            },
            {
                "symbol_id": btc_symbol_id,
                "exchange_id": binance_exchange_id,
                "ticker": "BTCBEUR",
            },
        ],
    )


def downgrade() -> None:
    connection = op.get_bind()

    btc_symbol_id = connection.execute(
        sa.text("SELECT id FROM symbols WHERE symbol='BTC'")
    ).scalar_one()
    binance_exchange_id = connection.execute(
        sa.text("SELECT id FROM exchanges WHERE name='Binance'")
    ).scalar_one()

    connection.execute(
        sa.text(
            "DELETE FROM tickers WHERE symbol_id=:symbol_id AND exchange_id=:exchange_id AND ticker IN ('BTCUSDT', 'BTCBEUR')"
        ),
        {"symbol_id": btc_symbol_id, "exchange_id": binance_exchange_id},
    )
    connection.execute(
        sa.text("DELETE FROM symbols WHERE id=:symbol_id"), {"symbol_id": btc_symbol_id}
    )
    connection.execute(
        sa.text("DELETE FROM exchanges WHERE id=:exchange_id"),
        {"exchange_id": binance_exchange_id},
    )
