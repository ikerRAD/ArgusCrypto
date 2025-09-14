from app.domain.crypto.models.ticker import Ticker
from app.infrastructure.crypto.database.table_models import TickerTableModel


class DbTickerTranslator:
    def bulk_translate_to_domain_model(
        self, ticker_table_models: list[TickerTableModel]
    ) -> list[Ticker]:
        return [
            self.translate_to_domain_model(ticker_table_model)
            for ticker_table_model in ticker_table_models
        ]

    def translate_to_domain_model(self, ticker_table_model: TickerTableModel) -> Ticker:
        return Ticker(
            id=ticker_table_model.id,
            symbol_id=ticker_table_model.symbol_id,
            exchange_id=ticker_table_model.exchange_id,
            ticker=ticker_table_model.ticker,
        )

    def translate_to_table_model(self, domain_ticker: Ticker) -> TickerTableModel:
        ticker_table_model = TickerTableModel(
            ticker=domain_ticker.ticker,
            exchange_id=domain_ticker.exchange_id,
            symbol_id=domain_ticker.symbol_id,
        )

        if domain_ticker.id is not None:
            ticker_table_model.id = domain_ticker.id

        return ticker_table_model
