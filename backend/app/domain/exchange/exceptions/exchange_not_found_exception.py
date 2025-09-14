class ExchangeNotFoundException(Exception):
    def __init__(self, attr_name, attr_value: str | int):
        super().__init__(f"exchange with {attr_name} '{attr_value}' not found")
