from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class DbExchangeRepository(ExchangeRepository):
    def find_exchange(self, exchange_name: str, fetch_tickers: bool) -> Exchange:
        with get_session() as session:
            statement = select(Exchange).where(Exchange.name == exchange_name)

            if fetch_tickers:
                statement = statement.options(selectinload(Exchange.tickers))

            query_result = session.execute(statement)
            exchange: Exchange | None = query_result.scalar_one_or_none()

            if exchange is None:
                raise ExchangeNotFoundException(exchange_name)

            return exchange
