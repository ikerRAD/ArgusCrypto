from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.domain.exchange.exceptions.exchange_not_found_exception import (
    ExchangeNotFoundException,
)
from app.domain.exchange.models import Exchange
from app.domain.exchange.repositories.exchange_repository import ExchangeRepository


class DbBinanceRepository(ExchangeRepository):
    __BINANCE_EXCHANGE_NAME = "Binance"

    def find_exchange(self, fetch_tickers=False) -> Exchange:
        with get_session() as session:
            statement = select(Exchange).where(
                Exchange.name == self.__BINANCE_EXCHANGE_NAME
            )

            if fetch_tickers:
                statement = statement.options(selectinload(Exchange.tickers))

            query_result = session.execute(statement)
            exchange: Exchange | None = query_result.scalar_one_or_none()

            if exchange is None:
                raise ExchangeNotFoundException(self.__BINANCE_EXCHANGE_NAME)

            return exchange
