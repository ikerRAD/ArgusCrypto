class SymbolNotFoundException(Exception):
    def __init__(self, symbol_id: int):
        super().__init__(f"Symbol not found for id '{symbol_id}'")
