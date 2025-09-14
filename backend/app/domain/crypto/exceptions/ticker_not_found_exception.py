

class TickerNotFoundException(Exception):
    def __init__(self, ticker_id: int):
        super().__init__(f"Ticker with id '{ticker_id}' not found.")