

class SymbolAlreadyExistsException(Exception):
    def __init__(self, symbol_symbol: str):
        super().__init__("Symbol '{}' already exists".format(symbol_symbol))
