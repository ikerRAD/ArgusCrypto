"""insert kraken exchange with some data

Revision ID: 56c8a737efdc
Revises: cf0e72a1385b
Create Date: 2025-09-12 15:02:01.628322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "56c8a737efdc"
down_revision: Union[str, Sequence[str], None] = "cf0e72a1385b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "exchanges",
            sa.column("name", sa.String),
        ),
        [
            {"name": "Kraken"},
        ],
    )

    connection = op.get_bind()
    btc_symbol_id = connection.execute(
        sa.text("SELECT id FROM symbols WHERE symbol='BTC'")
    ).scalar_one()
    kraken_exchange_id = connection.execute(
        sa.text("SELECT id FROM exchanges WHERE name='Kraken'")
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
                "exchange_id": kraken_exchange_id,
                "ticker": "XBTUSDT",
            },
            {
                "symbol_id": btc_symbol_id,
                "exchange_id": kraken_exchange_id,
                "ticker": "XXBTZEUR",
            },
        ],
    )


def downgrade() -> None:
    connection = op.get_bind()

    btc_symbol_id = connection.execute(
        sa.text("SELECT id FROM symbols WHERE symbol='BTC'")
    ).scalar_one()
    kraken_exchange_id = connection.execute(
        sa.text("SELECT id FROM exchanges WHERE name='Kraken'")
    ).scalar_one()

    connection.execute(
        sa.text(
            "DELETE FROM tickers WHERE symbol_id=:symbol_id AND exchange_id=:exchange_id AND ticker IN ('XBTUSDT', 'XXBTZEUR')"
        ),
        {"symbol_id": btc_symbol_id, "exchange_id": kraken_exchange_id},
    )
    connection.execute(
        sa.text("DELETE FROM exchanges WHERE id=:exchange_id"),
        {"exchange_id": kraken_exchange_id},
    )
