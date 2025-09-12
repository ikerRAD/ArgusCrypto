class ExchangeNotFoundException(Exception):
    def __init__(self, exchange_name: str):
        super().__init__(f"exchange with name '{exchange_name}' not found'")
