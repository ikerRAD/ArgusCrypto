class SymbolAlreadyExistsException(Exception):
    def __init__(self, symbol_symbol: str):
        super().__init__(f"Symbol '{symbol_symbol}' already exists")
