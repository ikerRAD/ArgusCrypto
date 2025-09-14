class TickerAlreadyExistsException(Exception):
    def __init__(self, ticker: str, exchange_id: int):
        super().__init__(
            f"Ticker '{ticker}' already exists for exchange '{exchange_id}'"
        )
